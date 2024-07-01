# Copyright 2024 INRAE, French National Research Institute for Agriculture, Food and Environment
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import bpy
import itertools
import os
import mathutils
import random
import math

from .plant_manager import PlantManager
from . import config
from .model_import import obj_import


class Beds:
    def __init__(self, field: config.Field):
        self.field = field
        self.bed_plant_groups = {}
        self.cur_bed_offset = 0.0
        self.center_pos = mathutils.Vector()
        self.width = 0.0
        self.length = 0.0
        self.assets_path = os.path.abspath('assets')
        self.rand = random.Random(random.getrandbits(32))
        self.plant_mgr = PlantManager()
        self.orientation_fns = {
            'random': lambda: self.rand.uniform(0, math.tau),
            'aligned': lambda: self.rand.choice([0.0, math.pi]),
            'zero': lambda: 0.0,
        }

    def load_plants(self):
        groups = set()
        for bed in self.field.beds:
            group = self.plant_mgr.get_group_by_height(bed.plant_type, bed.plant_height)

            if not group:
                raise RuntimeError(
                    "Error: plant type '{}' and height '{}' is unknown.".format(
                        bed.plant_type, bed.plant_height
                    )
                )

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
                obj_import(model.filepath)

    def create_beds(self):
        self.field.state = config.FieldState(beds=[])

        collection = bpy.data.collections['generated']

        for bed in self.field.beds:
            bed_object = self._create_bed(bed)
            collection.objects.link(bed_object)

    def get_center_pos(self):
        return mathutils.Vector((self.length / 2.0, self.width / 2.0, 0.0))

    def _create_bed(self, bed: config.Bed):
        noise = self.field.noise
        orientation_fn = self.orientation_fns[bed.orientation]
        row_offset = (bed.bed_width - (bed.rows_count - 1) * bed.row_distance) / 2.0

        vertices = []
        scales = []
        rotations = []
        indexes = []

        plant_group = self.plant_mgr.get_group_by_height(bed.plant_type, bed.plant_height)
        group_height = plant_group.average_height()
        nb_plants = len(plant_group.models)

        for bed_i in range(bed.beds_count):
            bed_state = config.BedState()

            for row_i in range(bed.rows_count):
                row_state = config.RowState()

                for plant_i in range(bed.plants_count):
                    if self.rand.random() < noise.missing:
                        continue

                    x = bed.offset[0] + plant_i * bed.plant_distance
                    y = bed.offset[1] + self.cur_bed_offset
                    y += bed_i * bed.bed_width + row_offset
                    y += bed.y_function(x) + row_i * bed.row_distance
                    z = bed.offset[2]

                    x += self.rand.normalvariate(0, noise.position)
                    y += self.rand.normalvariate(0, noise.position)
                    vertices.append((x, y, z))

                    scale = bed.plant_height / group_height
                    scale *= self.rand.lognormvariate(0, noise.scale)
                    scales.append(scale)

                    yaw = orientation_fn()
                    pitch = self.rand.normalvariate(0, noise.tilt)
                    roll = self.rand.normalvariate(0, noise.tilt)
                    rotations.extend([roll, pitch, yaw])

                    index = self.rand.randint(0, nb_plants - 1)
                    indexes.append(index)

                    plant_model = plant_group.models[index]

                    plant_state = config.PlantState(
                        x=x,
                        y=y,
                        z=z,
                        roll=roll,
                        pitch=pitch,
                        yaw=yaw,
                        height=plant_model.height * scale,
                        width=plant_model.width * scale,
                        leaf_area=plant_model.leaf_area * scale**2,
                        type=bed.plant_type,
                        filename=plant_model.filename,
                    )
                    row_state.crops.append(plant_state)
                    row_state.leaf_area += plant_state.leaf_area

                bed_state.rows.append(row_state)
                bed_state.leaf_area += row_state.leaf_area

            self.field.state.beds.append(bed_state)
            self.field.state.leaf_area += bed_state.leaf_area

        object = self._create_bed_object(vertices, bed.name, scales, rotations, indexes)

        cur_width = bed.beds_count * bed.bed_width
        self.width = max(self.width, self.cur_bed_offset + cur_width)
        self.length = max(self.length, (bed.plants_count - 1) * bed.plant_distance)
        if bed.shift_next_bed:
            self.cur_bed_offset += cur_width

        return object

    def _create_bed_object(self, vertices: list, name: str, scales, rotations, indexes):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices, edges=[], faces=[])
        mesh.update()

        scale_attr = mesh.attributes.new('scale', type='FLOAT', domain='POINT')
        scale_attr.data.foreach_set('value', scales)
        rotation_attr = mesh.attributes.new('rotation', type='FLOAT_VECTOR', domain='POINT')
        rotation_attr.data.foreach_set('vector', rotations)
        index_attr = mesh.attributes.new('index', type='INT', domain='POINT')
        index_attr.data.foreach_set('value', indexes)

        object = bpy.data.objects.new(name, mesh)

        # add and configure geometry nodes
        modifier = object.modifiers.new(name, 'NODES')
        modifier.node_group = bpy.data.node_groups['crops']

        collection_name = self.bed_plant_groups[name].full_name()
        plant_collection = bpy.data.collections[collection_name]
        modifier['Socket_2'] = plant_collection

        # apply plant material to the bed object
        active_material = plant_collection.objects[0].active_material
        if active_material:
            object.active_material = active_material.copy()

        return object
