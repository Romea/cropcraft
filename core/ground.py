import os
import bpy

from . import config


class Ground:

    def __init__(self, field: config.Field):
        self.weeds = field.weeds

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
                if model.endswith('.obj'):
                    bpy.ops.wm.obj_import(
                        filepath=os.path.join(group_path, model),
                        up_axis='Z',
                        forward_axis='Y',
                        use_split_objects=False,
                    )

    def create_plane(self, points: list):
        pass
