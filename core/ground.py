import os
import bpy
import random

from . import config
from .beds import Beds


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

    def __init__(self, field: config.Field, beds: Beds):
        self.field = field
        self.beds = beds

    def load_weeds(self):
        weeds_collection = bpy.data.collections['weeds']

        view_layer = bpy.context.view_layer
        scene_layer_coll = view_layer.layer_collection
        weeds_layer_coll = scene_layer_coll.children['resources'].children['weeds']

        weeds_path = os.path.join('assets', 'weeds')

        for group_name in os.listdir(weeds_path):
            collection = bpy.data.collections.new(group_name)
            weeds_collection.children.link(collection)
            group_layer_coll = weeds_layer_coll.children[group_name]

            group_path = os.path.join(weeds_path, group_name)
            models = filter(lambda x: x.endswith('.obj'), os.listdir(group_path))

            for model in models:
                view_layer.active_layer_collection = group_layer_coll
                bpy.ops.wm.obj_import(
                    filepath=os.path.join(group_path, model),
                    up_axis='Z',
                    forward_axis='Y',
                    use_split_objects=False,
                )

    def create_plane(self):
        object = create_plane_object('ground', self.beds.width, self.beds.length,
                                     self.field.headland_width)

        # create material
        mat = bpy.data.materials.new('ground')
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        tex_img = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_img.image = bpy.data.images.load(os.path.join('assets', 'textures', 'dirt.jpg'))
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_img.outputs['Color'])
        bsdf.inputs['Roughness'].default_value = 0.9
        object.active_material = mat

        # create UV
        bpy.types.UVProjector
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
        for weed in self.field.weeds:
            self.create_weed(weed)

    def create_weed(self, weed: config.Weed):
        object = create_plane_object(weed.name, self.beds.width, self.beds.length,
                                     self.field.scattering_extra_width)

        object.modifiers.new('grid', 'REMESH')

        node = object.modifiers.new('scattering', 'NODES')
        node.node_group = bpy.data.node_groups['scattering']
        node['Socket_3'] = bpy.data.collections[weed.plant_type]
        node['Socket_4'] = random.randint(-10000, 10000)

        collection = bpy.data.collections['generated']
        collection.objects.link(object)
