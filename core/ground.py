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

import os
import bpy
import random
import itertools

from . import config, input_utils
from .swaths import Swaths
from .model_import import obj_import


def create_plane_object(name: str, width: float, length: float, offset: float):
    vertices = [
        (-offset, -offset, 0.),
        (length + offset, -offset, 0.),
        (length + offset, width + offset, 0.),
        (-offset, width + offset, 0.),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    faces = [(0, 1, 2, 3)]

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges=edges, faces=faces)
    mesh.update()

    return bpy.data.objects.new(name, mesh)


class Ground:

    def __init__(self, field: config.Field, swaths: Swaths):
        self.field = field
        self.swaths = swaths
        self.assets_path = os.path.abspath('assets')
        self.rand = random.Random(random.getrandbits(32))

    def load_weeds(self):
        weeds_collection = bpy.data.collections['weeds']

        view_layer = bpy.context.view_layer
        scene_layer_coll = view_layer.layer_collection
        weeds_layer_coll = scene_layer_coll.children['resources'].children['weeds']

        selected_weed_types = [w.plant_type for w in self.field.weeds]

        assets_paths = os.scandir(os.path.join(self.assets_path, 'weeds'))

        user_weeds_dir = os.path.join(input_utils.user_data_dir(), 'weeds')
        if os.path.isdir(user_weeds_dir):
            local_paths = os.scandir()
        else:
            local_paths = []

        for weed_dir in itertools.chain(local_paths, assets_paths):
            if weed_dir.name not in selected_weed_types:
                continue

            collection = bpy.data.collections.new(weed_dir.name)
            weeds_collection.children.link(collection)
            group_layer_coll = weeds_layer_coll.children[weed_dir.name]

            models = filter(lambda x: x.endswith('.obj'), os.listdir(weed_dir.path))

            for model in models:
                view_layer.active_layer_collection = group_layer_coll
                obj_import(os.path.join(weed_dir.path, model))

    def load_stones(self):
        view_layer = bpy.context.view_layer
        scene_layer_coll = view_layer.layer_collection
        stones_layer_coll = scene_layer_coll.children['resources'].children['stones']

        stones_path = os.path.join(self.assets_path, 'stones')
        models = filter(lambda x: x.endswith('.obj'), os.listdir(stones_path))

        for model in models:
            view_layer.active_layer_collection = stones_layer_coll
            obj_import(os.path.join(stones_path, model))

    def create_plane(self):
        object = create_plane_object('ground', self.swaths.width, self.swaths.length,
                                     self.field.headland_width)

        # create material
        mat = bpy.data.materials.new('ground')
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        tex_img = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_img.image = bpy.data.images.load(os.path.realpath(os.path.join(self.assets_path, 'textures', 'dirt.jpg')))
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_img.outputs['Color'])
        bsdf.inputs['Roughness'].default_value = 0.9
        object.active_material = mat

        # create UV
        view_layer = bpy.context.view_layer
        view_layer.active_layer_collection = view_layer.layer_collection.children['resources']
        bpy.ops.mesh.primitive_plane_add()
        uv_object = bpy.data.objects['Plane']
        uv_object.name = 'uv_project'
        object.data.uv_layers.new(name='UVMap')
        uv_modifier = object.modifiers.new('UV', 'UV_PROJECT')
        uv_modifier.uv_layer = 'UVMap'
        uv_modifier.projectors[0].object = uv_object

        collection = bpy.data.collections['generated']
        collection.objects.link(object)

    def create_weeds(self):
        if self.field.weeds is None:
            return

        for weed in self.field.weeds:
            self.create_weed(weed)

    def create_weed(self, weed: config.Weed):
        object = create_plane_object(weed.name, self.swaths.width, self.swaths.length,
                                     self.field.scattering_extra_width)
        weed_collection = bpy.data.collections[weed.plant_type]

        object.modifiers.new('grid', 'REMESH')

        node = object.modifiers.new(weed.name, 'NODES')
        if weed.scattering_mode == 'noise':
            node.node_group = bpy.data.node_groups['scattering']
        else: #weed.scattering_mode == 'image':
            node.node_group = bpy.data.node_groups['scattering_from_image']

        node['Socket_3'] = weed_collection
        node['Socket_4'] = self.rand.randint(-10000, 10000)
        node['Socket_5'] = weed.distance_min
        node['Socket_6'] = weed.density
        if weed.scattering_mode == 'noise':
            node['Socket_7'] = weed.noise_scale
            node['Socket_8'] = weed.noise_offset
        else: #weed.scattering_mode == 'image':
            node['Socket_9'] = bpy.data.images.load(weed.scattering_img, check_existing=True)

        # apply instance material to the object
        for material in weed_collection.objects[0].data.materials:
            object.data.materials.append(material.copy())

        collection = bpy.data.collections['generated']
        collection.objects.link(object)

    def create_stones(self):
        if self.field.stones is None:
            return

        stones = self.field.stones

        object = create_plane_object('stones', self.swaths.width, self.swaths.length,
                                     self.field.scattering_extra_width)
        stones_collection = bpy.data.collections['stones']

        object.modifiers.new('grid', 'REMESH')

        node = object.modifiers.new('stones', 'NODES')
        node.node_group = bpy.data.node_groups['stones_scattering']
        node['Socket_2'] = stones_collection
        node['Socket_3'] = self.rand.randint(-10000, 10000)
        node['Socket_4'] = stones.distance_min
        node['Socket_5'] = stones.density
        node['Socket_6'] = stones.noise_scale
        node['Socket_7'] = stones.noise_offset

        # apply instance material to the object
        for material in stones_collection.objects[0].data.materials:
            object.data.materials.append(material.copy())

        collection = bpy.data.collections['generated']
        collection.objects.link(object)
