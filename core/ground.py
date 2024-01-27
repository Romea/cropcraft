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

        for group in os.listdir(os.path.join('assets', 'weeds')):
            group_name = os.path.basename(group)
            collection = bpy.data.collections.new(group_name)
            weeds_collection.children.link(collection)
            view_layer.active_layer_collection = weeds_layer_coll.children[group_name]

            for model_filepath in os.listdir(group):
                bpy.ops.wm.obj_import(
                    filepath=model_filepath,
                    up_axis='Z',
                    forward_axis='Y',
                    use_split_objects=False,
                )

    def create_plane(self, points: list):
        pass
