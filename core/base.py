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
from bpy.app.handlers import persistent
import mathutils

from . import geometry_nodes


def create_collections():
    generated = bpy.data.collections.new('generated')
    resources = bpy.data.collections.new('resources')
    plants = bpy.data.collections.new('plants')
    weeds = bpy.data.collections.new('weeds')
    stones = bpy.data.collections.new('stones')
    env = bpy.data.collections.new('env')
    scene = bpy.context.scene.collection

    scene.children.link(env)
    scene.children.link(resources)
    scene.children.link(generated)
    resources.children.link(plants)
    resources.children.link(weeds)
    resources.children.link(stones)

    view_layer = bpy.context.scene.view_layers['ViewLayer']
    view_layer.layer_collection.children['resources'].hide_viewport = True


def remove_all():
    for _, object in bpy.data.objects.items():
        bpy.data.objects.remove(object, do_unlink=True)
    for _, collection in bpy.data.collections.items():
        bpy.data.collections.remove(collection)


def create_camera(look_at: mathutils.Vector):
    camera_pos = mathutils.Vector((-13., look_at.y, 6.))
    look_dir = camera_pos - look_at
    look_quaternion = look_dir.to_track_quat('Z', 'Y')

    camera_data = bpy.data.cameras.new('camera')
    camera = bpy.data.objects.new('camera', camera_data)
    camera.location = camera_pos
    camera.rotation_euler = look_quaternion.to_euler()

    bpy.data.collections['env'].objects.link(camera)

    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    region = area.spaces[0].region_3d
    region.view_location = look_at
    region.view_distance = look_dir.length - 5.
    region.view_rotation = look_quaternion


def create_blender_context():
    remove_all()
    create_collections()
    geometry_nodes.create_all_node_group()
