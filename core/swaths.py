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


class Swaths:

    def __init__(self, field: config.Field):
        self.field = field
        self.swath_plant_groups = {}
        self.cur_swath_offset = 0.
        self.center_pos = mathutils.Vector()
        self.width = 0.
        self.length = 0.
        self.assets_path = os.path.abspath('assets')
        self.rand = random.Random(random.getrandbits(32))
        self.plant_mgr = PlantManager()
        self.orientation_fns = {
            'random': lambda: self.rand.uniform(0, math.tau),
            'aligned': lambda: self.rand.choice([0., math.pi]),
            'zero': lambda: 0.,
        }

    def load_plants(self):
        groups = set()
        for swath in self.field.swaths:
            group = self.plant_mgr.get_group_by_height(swath.plant_type, swath.plant_height)

            if not group:
                raise RuntimeError("Error: plant type '{}' and height '{}' is unknown.".format(
                    swath.plant_type, swath.plant_height))

            groups.add(group)
            self.swath_plant_groups[swath.name] = group

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

    def create_swaths(self):
        collection = bpy.data.collections['generated']

        for swath in self.field.swaths:
            swath_object = self.create_swath(swath)
            collection.objects.link(swath_object)

    def create_swath(self, swath: config.Swath):
        noise = self.field.noise
        orientation_fn = self.orientation_fns[swath.orientation]
        row_offset = (swath.swath_width - (swath.rows_count - 1) * swath.row_distance) / 2.

        id_tuples = itertools.product(
            range(swath.swaths_count),
            range(swath.rows_count),
            range(swath.plants_count),
        )
        vertices = []
        scales = []
        rotations = []

        plant_group = self.plant_mgr.get_group_by_height(swath.plant_type, swath.plant_height)
        group_height = plant_group.average_height()

        for swath_i, row_i, plant_i in id_tuples:
            if self.rand.random() < noise.missing:
                continue

            x = swath.offset[0] + plant_i * swath.plant_distance
            y = swath.offset[1] + self.cur_swath_offset + swath_i * swath.swath_width + row_offset
            y += swath.y_function(x) + row_i * swath.row_distance
            z = swath.offset[2]

            x += self.rand.normalvariate(0, noise.position)
            y += self.rand.normalvariate(0, noise.position)
            vertices.append((x, y, z))

            scale = swath.plant_height / group_height
            scale *= self.rand.lognormvariate(0, noise.scale)
            scales.append(scale)

            yaw = orientation_fn()
            pitch = self.rand.normalvariate(0, noise.tilt)
            roll = self.rand.normalvariate(0, noise.tilt)
            rotations.extend([roll, pitch, yaw])

        object = self.create_swath_object(vertices, swath.name, scales, rotations)

        cur_width = swath.swaths_count * swath.swath_width
        self.width = max(self.width, self.cur_swath_offset + cur_width)
        self.length = max(self.length, (swath.plants_count - 1) * swath.plant_distance)
        if swath.shift_next_swath:
            self.cur_swath_offset += cur_width

        return object

    def create_swath_object(self, vertices: list, name: str, scales, rotations):
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

        collection_name = self.swath_plant_groups[name].full_name()
        plant_collection = bpy.data.collections[collection_name]
        modifier['Socket_1'] = plant_collection

        # apply plant material to the swath object
        active_material = plant_collection.objects[0].active_material
        if active_material:
            object.active_material = active_material.copy()

        return object

    def get_center_pos(self):
        return mathutils.Vector((self.length / 2., self.width / 2., 0.))
