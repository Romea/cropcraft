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
import mathutils
import os
import math

from . import geometry_nodes


def create_blender_context():
    remove_all()
    create_collections()
    geometry_nodes.create_all_node_group()
    create_environment()

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.device = "GPU"

    # enable scene lights for material preview
    bpy.data.screens["Layout"].areas[3].spaces[0].shading.use_scene_lights = True


def remove_all():
    for _, object in bpy.data.objects.items():
        bpy.data.objects.remove(object, do_unlink=True)
    for _, collection in bpy.data.collections.items():
        bpy.data.collections.remove(collection)


def create_collections():
    generated = bpy.data.collections.new("generated")
    resources = bpy.data.collections.new("resources")
    plants = bpy.data.collections.new("plants")
    weeds = bpy.data.collections.new("weeds")
    stones = bpy.data.collections.new("stones")
    env = bpy.data.collections.new("env")
    scene = bpy.context.scene.collection

    scene.children.link(env)
    scene.children.link(resources)
    scene.children.link(generated)
    resources.children.link(plants)
    resources.children.link(weeds)
    resources.children.link(stones)

    view_layer = bpy.context.scene.view_layers["ViewLayer"]
    view_layer.layer_collection.children["resources"].hide_viewport = True
    resources.hide_render = True


def create_camera(look_at: mathutils.Vector):
    camera_pos = mathutils.Vector((-13.0, look_at.y, 6.0))
    look_dir = camera_pos - look_at
    look_quaternion = look_dir.to_track_quat("Z", "Y")

    camera_data = bpy.data.cameras.new("camera")
    camera = bpy.data.objects.new("camera", camera_data)
    camera.location = camera_pos
    camera.rotation_euler = look_quaternion.to_euler()

    bpy.data.collections["env"].objects.link(camera)

    area = next(area for area in bpy.context.screen.areas if area.type == "VIEW_3D")
    region = area.spaces[0].region_3d
    region.view_location = look_at
    region.view_distance = look_dir.length - 5.0
    region.view_rotation = look_quaternion


def create_environment():
    world = bpy.context.scene.world

    world.use_nodes = True
    bg = world.node_tree.nodes.new("ShaderNodeTexEnvironment")

    hdr_image_path = os.path.join(bpy.path.abspath("//"), "assets/textures/dry_hay_field_1k.hdr")
    hdr_image = bpy.data.images.load(hdr_image_path)

    bg.image = hdr_image
    output = world.node_tree.nodes.get("World Output")
    world.node_tree.links.new(bg.outputs[0], output.inputs[0])

    to_radians = math.pi / 180.0

    # Add sun light to the "env" collection
    env_collection = bpy.data.collections.get("env")
    if env_collection:
        sun_elevation = 30  # degrees
        sun_rotation = 47  # degrees

        sun_light_data = bpy.data.lights.new(name="sun", type="SUN")
        sun_light_data.color = (1.0, 0.954, 0.755)
        sun_light = bpy.data.objects.new(name="sun", object_data=sun_light_data)
        sun_light.data = sun_light_data
        env_collection.objects.link(sun_light)

        sun_light.data.energy = 13.0
        sun_light.rotation_euler = ((sun_elevation - 90) * to_radians, 0, sun_rotation * to_radians)
