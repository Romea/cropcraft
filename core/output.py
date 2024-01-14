from dataclasses import dataclass
import sys
import bpy
import os

from . import gazebo
from . import config


@dataclass
class BlenderFile:
    filename: str = None

    def export(self, output_dir: str):
        filepath = os.path.join(output_dir, self.filename)

        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=filepath)


@dataclass
class GazeboModel:
    name: str = None
    path: str = None
    author: str = None
    use_absolute_path: bool = None

    def export(self, output_dir: str):
        path = os.path.join(output_dir, self.path)
        collection = bpy.data.collections['generated']

        model = gazebo.GazeboModel(path, self.name, self.author, self.use_absolute_path)
        model.add_collection(collection)
        model.export_sdf()
        model.export_config()
