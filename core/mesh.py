import bpy


def export_usd(filepath, use_selection=False):
    bpy.ops.wm.usd_export(
        filepath=filepath,
        collection="generated",
        check_existing=False,
        selected_objects_only=use_selection,
    )


def export_obj(filepath, use_selection=False):
    bpy.ops.wm.obj_export(
        filepath=filepath,
        check_existing=False,
        apply_modifiers=True,
        up_axis="Z",
        forward_axis="Y",
        export_selected_objects=use_selection,
        export_materials=True,
    )


def export_stl(filepath, use_selection=False):
    bpy.ops.wm.stl_export(
        filepath=filepath,
        check_existing=False,
        apply_modifiers=True,
        up_axis="Z",
        forward_axis="Y",
        export_selected_objects=use_selection,
    )


def export_gltf(filepath, use_selection=False):
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        check_existing=False,
        export_apply=True,
        export_yup=False,
        use_selection=use_selection,
    )


_export_from_extension = {
    ".obj": export_obj,
    ".usd": export_usd,
    ".usda": export_usd,
    ".usdc": export_usd,
    ".usdz": export_usd,
    ".glb": export_gltf,
    ".gltf": export_gltf,
    ".stl": export_stl,
}


def export_from_extension(extension, filepath, use_selection=False):
    return _export_from_extension[extension](filepath, use_selection)


def extension_is_known(extension) -> bool:
    return extension in _export_from_extension
