import bpy
import itertools
import os
import mathutils
import random
import math

from .plant_model import get_plant_group
from . import config


class Beds:

    def __init__(self, field: config.Field):
        self.field = field
        self.bed_plant_groups = {}
        self.cur_bed_offset = 0.
        self.center_pos = mathutils.Vector()

    def load_plants(self):
        groups = set()
        for bed in self.field.beds:
            group = get_plant_group(bed.plant_type, bed.plant_height)

            if not group:
                raise RuntimeError("Error: plant type '{}' and height '{}' is unknown.".format(
                    bed.plant_type, bed.plant_height))

            groups.add(group)
            self.bed_plant_groups[bed.name] = group

        plants_collection = bpy.data.collections['plants']

        view_layer = bpy.context.view_layer
        scene_layer_coll = view_layer.layer_collection
        plants_layer_coll = scene_layer_coll.children['resources'].children['plants']

        for group in groups:
            full_name = group.full_name()
            collection = bpy.data.collections.new(full_name)
            plants_collection.children.link(collection)
            plant_layer_coll = plants_layer_coll.children[full_name]

            for model in group.models:
                view_layer.active_layer_collection = plant_layer_coll
                bpy.ops.wm.obj_import(
                    filepath=os.path.join('assets', 'plants', group.type, model.filename),
                    up_axis='Z',
                    forward_axis='Y',
                )

    def create_beds(self):
        collection = bpy.data.collections['generated']

        for bed in self.field.beds:
            bed_object = self.create_bed(bed)
            collection.objects.link(bed_object)

    def create_bed(self, bed: config.Bed):
        noise = self.field.noise
        row_half_width = (bed.rows_count - 1) * bed.row_distance / 2.

        id_tuples = itertools.product(
            range(bed.beds_count),
            range(bed.rows_count),
            range(bed.plants_count),
        )
        vertices = []
        scales = []
        rotations = []

        for bed_i, row_i, plant_i in id_tuples:
            if random.random() < noise.missing:
                continue

            x = plant_i * bed.plant_distance
            x += random.normalvariate(0, noise.position)
            y = self.cur_bed_offset + bed_i * bed.bed_width
            y += row_i * bed.row_distance - row_half_width
            y += random.normalvariate(0, noise.position)
            vertices.append((x, y, 0.))

            scales.append(random.lognormvariate(0, noise.scale))

            yaw = random.uniform(0, math.tau)
            pitch = random.normalvariate(0, noise.tilt)
            roll = random.normalvariate(0, noise.tilt)
            rotations.extend([roll, pitch, yaw])

        object = self.create_bed_object(vertices, bed.name, scales, rotations)

        # increase bed offset for the next bed
        if bed.shift_next_bed:
            self.cur_bed_offset += bed.beds_count * bed.bed_width

        self.update_center_pos(bed.bed_width, (bed.plants_count - 1) * bed.plant_distance)

        return object

    def create_bed_object(self, vertices: list, name: str, scales, rotations):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices, edges=[], faces=[])
        mesh.update()

        scale_attr = mesh.attributes.new('scale', type='FLOAT', domain='POINT')
        scale_attr.data.foreach_set('value', scales)
        rotation_attr = mesh.attributes.new('rotation', type='FLOAT_VECTOR', domain='POINT')
        rotation_attr.data.foreach_set('vector', rotations)

        object = bpy.data.objects.new(name, mesh)

        # add and configure geometry nodes
        modifier = object.modifiers.new(name, 'NODES')
        modifier.node_group = bpy.data.node_groups['crops']

        collection_name = self.bed_plant_groups[name].full_name()
        plant_collection = bpy.data.collections[collection_name]
        modifier['Socket_1'] = plant_collection

        # apply plant material to the bed object
        object.active_material = plant_collection.objects[0].active_material.copy()

        return object

    def update_center_pos(self, bed_width: float, row_length: float):
        self.center_pos.x = max(self.center_pos.x, row_length / 2.)
        self.center_pos.y = (self.cur_bed_offset - bed_width) / 2.
