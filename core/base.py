import bpy

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

    resources.hide_viewport = True
    resources.hide_render = True


def remove_all():
    for _, object in bpy.data.objects.items():
        bpy.data.objects.remove(object, do_unlink=True)
    for _, collection in bpy.data.collections.items():
        bpy.data.collections.remove(collection)


def create_blender_context():
    remove_all()
    create_collections()
    geometry_nodes.create_all_node_group()
