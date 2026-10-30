#!/usr/bin/env python3
"""
Build a texture atlas from an OBJ+MTL with multiple diffuse textures.

Features:
- Packs all map_Kd images (diffuse) into a single atlas (vertical, horizontal, or simple 'row' pack).
- Adjusts each face's UVs. Safe approach: duplicates vt entries per face so that
  material-specific scaling/offset never corrupts shared UVs.
- Optionally merges all materials into one atlas material.
- Writes:
    <output_prefix>.obj
    <output_prefix>.mtl
    <output_prefix>_atlas.jpg
    <output_prefix>_atlas_layout.json (regions, for debugging)

Limitations / Simplifications:
- Only processes map_Kd (diffuse). Normal/roughness/etc can be added similarly (see comments).
- No advanced bin packing; modes: vertical, horizontal, or uniform grid heuristic.
- Expects faces with texture coordinates (v/vt[/vn]). If absent, cannot remap.
- If a vt is reused by multiple materials, duplication logic prevents conflicts.
"""

import argparse
import os
import re
import json
from math import ceil, sqrt
from collections import OrderedDict
from PIL import Image

# ---------------------------------------------------------
# Helpers for parsing
# ---------------------------------------------------------
_face_re = re.compile(r'^f\s+')
_usemtl_re = re.compile(r'^usemtl\s+(\S+)')
_mtllib_re = re.compile(r'^mtllib\s+(\S+)')
_vt_token_re = re.compile(r'^vt\s+')
_comment_re = re.compile(r'^\s*#')

def parse_mtl(mtl_path):
    """
    Parse MTL file; return ordered dict:
    materials[name] = {
        'lines': [raw lines],
        'map_Kd': 'path/texture.jpg' or None,
        ... (we keep entire block to preserve other properties)
    }
    """
    materials = OrderedDict()
    current = None
    if not os.path.isfile(mtl_path):
        raise FileNotFoundError(f"MTL not found: {mtl_path}")
    with open(mtl_path, 'r', encoding='utf-8', errors='ignore') as f:
        for raw_line in f:
            line = raw_line.rstrip('\n')
            if line.startswith('newmtl '):
                name = line.split(None, 1)[1].strip()
                current = {
                    'name': name,
                    'lines': [line],
                    'map_Kd': None
                }
                materials[name] = current
            else:
                if current is not None:
                    # Track map_Kd
                    if line.lower().startswith('map_kd'):
                        # Extract filename (allow options)
                        parts = line.split()
                        # Usually map_Kd <file>; handle optional parameters
                        tex_file = parts[-1]
                        current['map_Kd'] = tex_file
                    current['lines'].append(line)
    return materials

def load_images(materials, search_dir):
    """
    Load images for each map_Kd. Return dict material_name->PIL.Image
    Also return unique texture list mapping actual file -> PIL.Image to deduplicate.
    """
    mat_images = {}
    tex_cache = {}
    for mname, m in materials.items():
        tex = m['map_Kd']
        if tex is None:
            continue
        tex_path = tex
        if not os.path.isabs(tex_path):
            tex_path = os.path.join(search_dir, tex_path)
        if not os.path.isfile(tex_path):
            raise FileNotFoundError(f"Texture file not found for material '{mname}': {tex_path}")
        if tex_path not in tex_cache:
            tex_cache[tex_path] = Image.open(tex_path).convert("RGBA")
        mat_images[mname] = tex_cache[tex_path]
    return mat_images

def pack_textures(mat_images, mode='vertical', padding=4, pow2=False, background=(255,255,255,255)):
    """
    Simple packing strategies:
      - vertical: stack textures top->bottom
      - horizontal: left->right
      - grid: square-ish grid
    Returns:
      atlas_img (PIL.Image),
      layout dict: { material_name: { 'x': int, 'y': int, 'w': int, 'h': int } }
    Coordinates (x,y) are top-left in atlas pixel space.
    """
    items = list(mat_images.items())

    if mode == 'vertical':
        width = max(im.width for _, im in items)
        height = sum(im.height for _, im in items) + padding * (len(items)-1 if len(items)>1 else 0)
        atlas = Image.new("RGBA", (width, height), background)
        layout = {}
        y = 0
        for name, im in items:
            atlas.paste(im, (0, y))
            layout[name] = {'x': 0, 'y': y, 'w': im.width, 'h': im.height}
            y += im.height + padding

    elif mode == 'horizontal':
        width = sum(im.width for _, im in items) + padding * (len(items)-1 if len(items)>1 else 0)
        height = max(im.height for _, im in items)
        atlas = Image.new("RGBA", (width, height), background)
        layout = {}
        x = 0
        for name, im in items:
            atlas.paste(im, (x, 0))
            layout[name] = {'x': x, 'y': 0, 'w': im.width, 'h': im.height}
            x += im.width + padding

    elif mode == 'grid':
        n = len(items)
        cols = int(ceil(sqrt(n)))
        rows = int(ceil(n / cols))
        max_w = max(im.width for _, im in items)
        max_h = max(im.height for _, im in items)
        width = cols * max_w + padding * (cols - 1)
        height = rows * max_h + padding * (rows - 1)
        atlas = Image.new("RGBA", (width, height), background)
        layout = {}
        for idx, (name, im) in enumerate(items):
            r = idx // cols
            c = idx % cols
            x = c * (max_w + padding)
            y = r * (max_h + padding)
            atlas.paste(im, (x, y))
            layout[name] = {'x': x, 'y': y, 'w': im.width, 'h': im.height}
    else:
        raise ValueError(f"Unknown pack mode: {mode}")

    if pow2:
        new_w = 1
        while new_w < atlas.width: new_w <<= 1
        new_h = 1
        while new_h < atlas.height: new_h <<= 1
        if new_w != atlas.width or new_h != atlas.height:
            pow2_atlas = Image.new("RGBA", (new_w, new_h), background)
            pow2_atlas.paste(atlas, (0,0))
            atlas = pow2_atlas

    return atlas, layout

def parse_obj_collect(obj_path):
    """
    Read OBJ lines; keep everything for rewriting.
    Return:
      lines (list[str])
    """
    if not os.path.isfile(obj_path):
        raise FileNotFoundError(f"OBJ not found: {obj_path}")
    with open(obj_path, 'r', encoding='utf-8', errors='ignore') as f:
        return [l.rstrip('\n') for l in f]

def build_material_usage(lines):
    """
    Scan OBJ lines; record for each face the material active at that time.
    Return list of dict for each line:
       [
         {'type': 'other', 'text': original_line},
         {'type': 'usemtl', 'material': name, 'text': line},
         {'type': 'face', 'material': current_material, 'text': line, 'tokens': [...]}
       ]
    """
    structured = []
    current_mtl = None
    for line in lines:
        if _comment_re.match(line) or not line.strip():
            structured.append({'type': 'other', 'text': line})
            continue
        um = _usemtl_re.match(line)
        if um:
            current_mtl = um.group(1)
            structured.append({'type': 'usemtl', 'material': current_mtl, 'text': line})
        elif _face_re.match(line):
            structured.append({'type': 'face', 'material': current_mtl, 'text': line})
        else:
            structured.append({'type': 'other', 'text': line})
    return structured

def extract_vt(lines):
    """
    Extract vt lines (u v [w]) into list so we know how many existed (if we wanted in-place edits).
    We are going to DUPLICATE vt per face vertex anyway, so we just track original count.
    """
    vt_count = 0
    for l in lines:
        if _vt_token_re.match(l):
            vt_count += 1
    return vt_count

def remap_obj(structured_lines, atlas_layout, atlas_w, atlas_h, merge_materials=False, merged_material_name="atlas_material"):
    """
    Create new OBJ with:
       - New mtllib reference (we will set later)
       - Optionally unify usemtl into one
       - Duplicate vt for each face vertex with adjusted (u,v)
    Returns:
      new_lines
    """
    new_lines = []
    # We'll postpone writing mtllib until caller adds it.
    # We'll accumulate new vt lines at end (or we can stream them inserted where faces appear).
    vt_entries = []
    new_face_lines = []

    def remap_uv(old_u, old_v, region):
        # region.x/y top-left. We must translate y to bottom-based.
        x, y, w, h = region['x'], region['y'], region['w'], region['h']
        # Convert: original (u,v) assumed in [0,1]. Scale inside region.
        # Region in normalized coordinate: offset_x = x/atlas_w, etc.
        region_x = x / atlas_w
        region_y_top = y / atlas_h
        region_h_norm = h / atlas_h
        region_w_norm = w / atlas_w
        # OBJ v=0 is bottom; atlas y=0 is top. region_y from top; need bottom offset:
        region_y = 1.0 - ( (y + h) / atlas_h )  # bottom of region
        # new_u, new_v
        nu = region_x + old_u * region_w_norm
        nv = region_y + old_v * region_h_norm
        return nu, nv

    for entry in structured_lines:
        if entry['type'] == 'other':
            # Remove old vt lines (we will append new ones later)
            if _vt_token_re.match(entry['text']):
                continue
            # Remove old mtllib lines; caller will add new one.
            if _mtllib_re.match(entry['text']):
                continue
            new_lines.append(entry['text'])
        elif entry['type'] == 'usemtl':
            if merge_materials:
                # Defer writing; we'll write single usemtl once before first face that had a material.
                # Easiest: skip here; add one at the very end (or before first face).
                continue
            else:
                new_lines.append(f"usemtl {entry['material']}")
        elif entry['type'] == 'face':
            mat = entry['material']
            if mat not in atlas_layout:
                # Face with material that had no texture; leave face but no UV remap (just copy).
                # We still must parse to duplicate vt if face has vt indices. If not, just copy line.
                # If no vt indices, we can just keep face line as-is.
                if '/' not in entry['text']:
                    new_lines.append(entry['text'])
                else:
                    # Duplicate anyway (safe). We'll parse tokens.
                    face_line = entry['text']
                    parts = face_line.split()
                    face_tokens = parts[1:]
                    new_face_spec = []
                    for ft in face_tokens:
                        # ft like v/t/n or v//n or v/t
                        v_idx, vt_idx, vn_idx = parse_face_triplet(ft)
                        # Without original vt we cannot do new uv; just reuse same indices.
                        # We'll skip duplication since there's no region mapping.
                        new_face_spec.append(ft)
                    new_lines.append("f " + " ".join(new_face_spec))
                continue

            region = atlas_layout[mat]

            # Parse face, build new vt entries
            parts = entry['text'].split()
            face_tokens = parts[1:]
            new_face_spec = []
            for ft in face_tokens:
                v_idx, vt_idx, vn_idx = parse_face_triplet(ft)

                if vt_idx is None:
                    # No texture coordinate in this face vertex; create one at (0,0)
                    old_u, old_v = 0.0, 0.0
                else:
                    # We do not need original vt values if we remap relative coordinates per material only if we had them.
                    # Proper approach: we *must* read original vt lines to get old_u, old_v.
                    # Because we duplicated per face, simpler is to load original vt lines into array.
                    # But for safety, let's store them globally: we need the original vt list.
                    # This function is called AFTER we know we want to remap; We'll rely on a global array (closure) old_vt_list
                    old_u, old_v = old_vt_list[vt_idx - 1]  # 1-based index in OBJ

                nu, nv = remap_uv(old_u, old_v, region)
                vt_entries.append((nu, nv))
                new_vt_index = len(vt_entries)  # 1-based after we later write them
                # Reconstruct token
                if vn_idx is not None:
                    new_face_spec.append(f"{v_idx}/{new_vt_index}/{vn_idx}")
                else:
                    new_face_spec.append(f"{v_idx}/{new_vt_index}")

            new_face_lines.append("f " + " ".join(new_face_spec))

    # Insert single merged usemtl if requested (before first face we appended)
    if merge_materials:
        # Find position to inject: after last mtllib or after first non-comment
        insertion_index = 0
        for i, l in enumerate(new_lines):
            if l.startswith('o ') or l.startswith('g ') or l.startswith('v '):
                insertion_index = i
                break
        new_lines.insert(insertion_index, f"usemtl {merged_material_name}")

    # Append new vt lines after all geometry (keep order: v, vt, vn, then faces)
    # Find index of first face line to place vt before (optional). Simpler: append vt before faces.
    first_face_idx = len(new_lines)
    for i, l in enumerate(new_lines):
        if l.startswith('f '):
            first_face_idx = i
            break

    vt_lines = [f"vt {u:.6f} {v:.6f}" for (u, v) in vt_entries]
    new_lines[first_face_idx:first_face_idx] = vt_lines
    # Finally add face lines
    new_lines.extend(new_face_lines)

    return new_lines

def parse_face_triplet(token):
    """
    Parse face vertex token: v, v/t, v//n, v/t/n
    Return (v_idx, vt_idx or None, vn_idx or None)
    """
    if '//' in token:
        v_part, vn_part = token.split('//', 1)
        return int(v_part), None, int(vn_part)
    parts = token.split('/')
    if len(parts) == 1:
        return int(parts[0]), None, None
    if len(parts) == 2:
        v_idx, vt_idx = parts
        return int(v_idx), int(vt_idx), None
    if len(parts) == 3:
        v_idx, vt_idx, vn_idx = parts
        vt_i = int(vt_idx) if vt_idx != '' else None
        vn_i = int(vn_idx) if vn_idx != '' else None
        return int(v_idx), vt_i, vn_i
    raise ValueError(f"Cannot parse face token: {token}")

# Will hold original vt coords for remapping (closure variable for remap_obj)
old_vt_list = []

def load_original_vt(lines):
    global old_vt_list
    old_vt_list = []
    for l in lines:
        if l.startswith('vt '):
            parts = l.split()
            if len(parts) < 3:
                continue
            u = float(parts[1])
            v = float(parts[2])
            old_vt_list.append((u, v))
    return len(old_vt_list)

def write_new_mtl(original_materials, out_mtl_path, atlas_filename, layout, merge_materials=False, merged_material_name="atlas_material"):
    with open(out_mtl_path, 'w', encoding='utf-8') as f:
        f.write("# Generated MTL with texture atlas\n")
        if merge_materials:
            f.write(f"newmtl {merged_material_name}\n")
            f.write("Ka 1.000 1.000 1.000\nKd 1.000 1.000 1.000\nKs 0.000 0.000 0.000\n")
            f.write(f"map_Kd {atlas_filename}\n")
            f.write("\n")
        else:
            for name, mat in original_materials.items():
                f.write(f"newmtl {name}\n")
                # Copy non-map_Kd lines except newmtl
                for line in mat['lines']:
                    if line.startswith('newmtl'):
                        continue
                    lower = line.lower()
                    if lower.startswith('map_kd'):
                        continue  # we will replace
                    f.write(line + "\n")
                f.write(f"map_Kd {atlas_filename}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Build a texture atlas for an OBJ+MTL.")
    parser.add_argument('--obj', required=True, help="Input OBJ file")
    parser.add_argument('--mtl', required=True, help="Input MTL file (referenced by OBJ)")
    parser.add_argument('--output-prefix', required=True, help="Prefix for output files")
    parser.add_argument('--pack-mode', choices=['vertical','horizontal','grid'], default='vertical')
    parser.add_argument('--padding', type=int, default=8)
    parser.add_argument('--pow2', action='store_true', help="Expand atlas to next power-of-two dimensions")
    parser.add_argument('--merge-materials', action='store_true', help="Merge all materials into a single one")
    parser.add_argument('--atlas-filename', default='atlas.jpg', help="Filename for atlas image (inside same output directory)")
    parser.add_argument('--background', default='255,255,255', help="Background color R,G,B (default white)")
    args = parser.parse_args()

    obj_path = args.obj
    mtl_path = args.mtl
    out_prefix = args.output_prefix
    out_dir = os.path.dirname(os.path.abspath(out_prefix))
    os.makedirs(out_dir, exist_ok=True)

    background_rgb = tuple(int(c) for c in args.background.split(',')) + (255,)

    # 1. Parse materials
    materials = parse_mtl(mtl_path)

    # 2. Load images
    mat_images = load_images(materials, search_dir=os.path.dirname(os.path.abspath(mtl_path)))
    if not mat_images:
        raise RuntimeError("No map_Kd textures found in the provided MTL.")

    # 3. Pack
    atlas_img, layout = pack_textures(
        mat_images,
        mode=args.pack_mode,
        padding=args.padding,
        pow2=args.pow2,
        background=background_rgb
    )

    atlas_path = out_prefix + "_" + args.atlas_filename
    atlas_img.convert("RGB").save(atlas_path, quality=95)
    print(f"[INFO] Wrote atlas: {atlas_path}")

    # 4. Parse OBJ
    obj_lines = parse_obj_collect(obj_path)
    # Load original vt
    num_vt = load_original_vt(obj_lines)
    if num_vt == 0:
        print("[WARN] No existing vt coordinates found. Cannot remap UVs. Exiting.")
        return

    structured = build_material_usage(obj_lines)

    # 5. Remap / rewrite OBJ
    new_obj_lines = remap_obj(
        structured,
        atlas_layout=layout,
        atlas_w=atlas_img.width,
        atlas_h=atlas_img.height,
        merge_materials=args.merge_materials
    )

    # Insert new mtllib line at top (or after comments)
    out_mtl_name = os.path.basename(out_prefix) + ".mtl"
    inserted = False
    for i, l in enumerate(new_obj_lines):
        if l.startswith('mtllib'):
            new_obj_lines[i] = f"mtllib {out_mtl_name}"
            inserted = True
            break
    if not inserted:
        # Insert near top
        insertion_point = 0
        while insertion_point < len(new_obj_lines) and new_obj_lines[insertion_point].startswith('#'):
            insertion_point += 1
        new_obj_lines.insert(insertion_point, f"mtllib {out_mtl_name}")

    out_obj_path = out_prefix + ".obj"
    with open(out_obj_path, 'w', encoding='utf-8') as f:
        for line in new_obj_lines:
            f.write(line + "\n")
    print(f"[INFO] Wrote new OBJ: {out_obj_path}")

    # 6. Write new MTL
    out_mtl_path = out_prefix + ".mtl"
    write_new_mtl(
        original_materials=materials,
        out_mtl_path=out_mtl_path,
        atlas_filename=os.path.basename(atlas_path),
        layout=layout,
        merge_materials=args.merge_materials
    )
    print(f"[INFO] Wrote new MTL: {out_mtl_path}")

    # 7. Write layout JSON (optional)
    layout_json_path = out_prefix + "_atlas_layout.json"
    norm_layout = {}
    for m, r in layout.items():
        norm_layout[m] = {
            'x_px': r['x'], 'y_px': r['y'], 'w_px': r['w'], 'h_px': r['h'],
            'x_norm': r['x']/atlas_img.width, 'y_norm_top': r['y']/atlas_img.height,
            'w_norm': r['w']/atlas_img.width, 'h_norm': r['h']/atlas_img.height,
            'y_norm_bottom': (atlas_img.height - (r['y'] + r['h'])) / atlas_img.height
        }
    with open(layout_json_path, 'w', encoding='utf-8') as jf:
        json.dump({
            'atlas_width': atlas_img.width,
            'atlas_height': atlas_img.height,
            'materials': norm_layout
        }, jf, indent=2)
    print(f"[INFO] Wrote atlas layout JSON: {layout_json_path}")

    print("[DONE] Texture atlas build complete.")

if __name__ == '__main__':
    main()