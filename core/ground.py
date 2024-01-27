import os
import bpy

from . import config


class Ground:

    def __init__(self, field: config.Field):
        self.field = field

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

    def create_plane(self, width: float, length: float):
        offset = self.field.headland_width
        vertices = [
            (-offset, -offset, 0.),
            (length + offset, -offset, 0.),
            (length + offset, width + offset, 0.),
            (-offset, width + offset, 0.),
        ]
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        faces = [(0, 1, 2, 3)]

        mesh = bpy.data.meshes.new('ground')
        mesh.from_pydata(vertices, edges=edges, faces=faces)
        mesh.update()

        material = bpy.data.materials.new('ground')
        object = bpy.data.objects.new('ground', mesh)
        object.active_material = material

        collection = bpy.data.collections['generated']
        collection.objects.link(object)
