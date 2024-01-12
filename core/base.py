import bpy
from bpy.app.handlers import persistent
import mathutils

from . import geometry_nodes


def create_collections():
    generated = bpy.data.collections.new('generated')
    resources = bpy.data.collections.new('resources')
    plants = bpy.data.collections.new('plants')
    weeds = bpy.data.collections.new('weeds')
    env = bpy.data.collections.new('env')
    scene = bpy.context.scene.collection

    scene.children.link(env)
    scene.children.link(resources)
    scene.children.link(generated)
    resources.children.link(plants)
    resources.children.link(weeds)

    view_layer = bpy.context.scene.view_layers['ViewLayer']
    view_layer.layer_collection.children['resources'].hide_viewport = True


def remove_all():
    for _, object in bpy.data.objects.items():
        bpy.data.objects.remove(object, do_unlink=True)
    for _, collection in bpy.data.collections.items():
        bpy.data.collections.remove(collection)


def create_camera(look_at: mathutils.Vector):
    camera_pos = mathutils.Vector((-10., look_at.y, 7.))
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
