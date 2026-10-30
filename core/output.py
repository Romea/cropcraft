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

from dataclasses import dataclass
import bpy
import os

from . import gazebo
from . import config
from .field_description import FieldDescription


@dataclass
class BlenderFile:
    filename: str = None

    def export(self, output_dir: str, field: config.Field):
        filepath = os.path.join(output_dir, self.filename)

        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=filepath)


@dataclass
class GazeboModel:
    name: str = None
    path: str = None
    author: str = None
    use_absolute_path: bool = None
    ignition_mode: bool = None

    def export(self, output_dir: str, field: config.Field):
        path = os.path.join(output_dir, self.path)

        model = gazebo.GazeboModel(path, self.name, self.author, self.use_absolute_path, self.ignition_mode)
        model.export_field(field)
        model.generate_sdf()
        model.generate_config()


@dataclass
class USDFile:
    filename: str = None

    def export(self, output_dir: str, field: config.Field):
        filepath = os.path.join(output_dir, self.filename)

        bpy.ops.file.pack_all()
        bpy.ops.wm.usd_export(
            filepath=filepath,
            collection="generated"
        )


@dataclass
class Description:
    filename: str = None
    format: str = None

    def export(self, output_dir: str, field: config.Field):
        filepath = os.path.join(output_dir, self.filename)

        description = FieldDescription(field)
        description.dump(filepath, self.format)
