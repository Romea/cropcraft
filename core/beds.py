import bpy
import itertools


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


def create_beds(cfg: dict):
    field = cfg['field']

    collection = bpy.data.collections.new('generated')
    bpy.context.scene.collection.children.link(collection)

    for name, bed in field['beds'].items():
        bed_object = create_bed(name, bed, field)
        collection.objects.link(bed_object)
