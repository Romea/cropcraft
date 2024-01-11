import bpy
import itertools
import os
import sys

from .plant_model import get_plant_group


def load_plants(field: dict):
    groups = set()
    for _, bed in field['beds'].items():
        group = get_plant_group(bed['plant_type'], bed['plant_height'])

        if not group:
            msg = "Error: plant type '{}' and height '{}' is unknown.".format(
                bed['plant_type'], bed['plant_height'])
            print(msg, file=sys.stderr)
            continue
        
        groups.add(group)

    plants_collection = bpy.data.collections['plants']

    scene_layer_coll = bpy.context.view_layer.layer_collection
    plants_layer_coll = scene_layer_coll.children['resources'].children['plants']

    for group in groups:
        collection = bpy.data.collections.new(group.name)
        plants_collection.children.link(collection)
        bpy.context.view_layer.active_layer_collection = plants_layer_coll.children[group.name]

        objects = []
        for model in group.models:
            object = bpy.ops.wm.obj_import(
                filepath=os.path.join('assets', 'plants', group.type, model.filename),
                up_axis='Z',
                forward_axis='X',
            )
            objects.append(object)



def create_bed(name: str, bed: dict, field: dict):
    plants_count = bed['plants_count']
    rows_count = bed['rows_count']
    beds_count = bed['beds_count']
    plant_dist = bed['plant_distance']
    row_dist = bed['row_distance']
    bed_width = field['bed_width']

    row_half_width = (rows_count - 1) * row_dist / 2.

    def plant_position(bed_ind, row_ind, plant_ind):
        return [
            plant_ind * plant_dist,
            bed_ind * bed_width - row_half_width + row_ind * row_dist,
            0.,
        ]

    id_tuples = itertools.product(range(beds_count), range(rows_count), range(plants_count))
    vertices = list(map(lambda ids: plant_position(*ids), id_tuples))

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges=[], faces=[])
    mesh.update()

    return bpy.data.objects.new(name, mesh)


def create_beds(field: dict):
    collection = bpy.data.collections['generated']

    for name, bed in field['beds'].items():
        bed_object = create_bed(name, bed, field)
        collection.objects.link(bed_object)
