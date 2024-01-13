import bpy
import itertools
import os
import sys
import mathutils

from .plant_model import get_plant_group


class Beds:

    def __init__(self, field: dict):
        self.field = field
        self.bed_plant_groups = {}
        self.cur_bed_offset = 0.
        self.center_pos = mathutils.Vector()

    def load_plants(self):
        groups = set()
        for bed_name, bed in self.field['beds'].items():
            group = get_plant_group(bed['plant_type'], bed['plant_height'])

            if not group:
                msg = "Error: plant type '{}' and height '{}' is unknown.".format(
                    bed['plant_type'], bed['plant_height'])
                print(msg, file=sys.stderr)
                continue

            groups.add(group)
            self.bed_plant_groups[bed_name] = group

        plants_collection = bpy.data.collections['plants']

        view_layer = bpy.context.view_layer
        scene_layer_coll = view_layer.layer_collection
        plants_layer_coll = scene_layer_coll.children['resources'].children['plants']

        for group in groups:
            full_name = group.full_name()
            collection = bpy.data.collections.new(full_name)
            plants_collection.children.link(collection)
            view_layer.active_layer_collection = plants_layer_coll.children[full_name]

            for model in group.models:
                bpy.ops.wm.obj_import(
                    filepath=os.path.join('assets', 'plants', group.type, model.filename),
                    up_axis='Z',
                    forward_axis='X',
                )

    def create_beds(self):
        collection = bpy.data.collections['generated']

        for name, bed in self.field['beds'].items():
            bed_object = self.create_bed(name, bed)
            collection.objects.link(bed_object)

    def create_bed(self, name: str, bed: dict):
        plants_count = bed['plants_count']
        rows_count = bed['rows_count']
        beds_count = bed['beds_count']
        plant_dist = bed['plant_distance']
        row_dist = bed['row_distance']
        bed_width = bed['bed_width'] if 'bed_width' in bed else self.field['bed_width']

        row_half_width = (rows_count - 1) * row_dist / 2.

        def plant_position(bed_ind, row_ind, plant_ind):
            return [
                plant_ind * plant_dist,
                self.cur_bed_offset + bed_ind * bed_width - row_half_width + row_ind * row_dist,
                0.,
            ]

        id_tuples = itertools.product(range(beds_count), range(rows_count), range(plants_count))
        vertices = list(map(lambda ids: plant_position(*ids), id_tuples))

        object = self.create_bed_object(vertices, name)

        # increase bed offset for the next bed
        self.cur_bed_offset += beds_count * bed_width

        self.update_center_pos(bed_width, (plants_count - 1) * plant_dist)

        return object

    def create_bed_object(self, vertices: list, name: str):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices, edges=[], faces=[])
        mesh.update()

        object = bpy.data.objects.new(name, mesh)

        # add and configure geometry nodes
        modifier = object.modifiers.new(name, 'NODES')
        modifier.node_group = bpy.data.node_groups['crops']

        collection_name = self.bed_plant_groups[name].full_name()
        plant_collection = bpy.data.collections[collection_name]
        modifier["Socket_2"] = plant_collection

        # apply plant material to the bed object
        object.active_material = plant_collection.objects[0].active_material.copy()

        # # copy UVMap from
        # attrUV = target.data.attributes["UVMap"].data
        # targetUV = target.data.uv_layers[0].data 
        # for i, elem in enumerate(targetUV):
        #     elem.uv = attrUV[i].vector

        return object

    def update_center_pos(self, bed_width: float, row_length: float):
        self.center_pos.x = max(self.center_pos.x, row_length / 2.)
        self.center_pos.y = (self.cur_bed_offset - bed_width) / 2.
