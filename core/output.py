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
from . import mesh
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

    def export(self, output_dir: str, field: config.Field):
        path = os.path.join(output_dir, self.path)

        model = gazebo.GazeboModel(path, self.name, self.author, self.use_absolute_path)
        model.export_field(field)
        model.generate_sdf()
        model.generate_config()


@dataclass
class Description:
    filename: str = None
    format: str = None

    def export(self, output_dir: str, field: config.Field):
        filepath = os.path.join(output_dir, self.filename)

        description = FieldDescription(field)
        description.dump(filepath, self.format)


class Mesh:
    def __init__(self) -> None:
        self._filename = None
        self._extension = None

    def export(self, output_dir: str, field: config.Field):
        filepath = os.path.join(output_dir, self.filename)
        _, extension = os.path.splitext(filepath)

        bpy.ops.file.pack_all()
        mesh.export_from_extension(extension, filepath, use_selection=False)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, name):
        self._filename = name
        _, self._extension = os.path.splitext(self._filename)

        if not self._extension:
            raise ValueError(f"No extension provided on mesh file '{self._filename}")

        if not mesh.extension_is_known(self._extension):
            raise ValueError(
                f"Unknown extension '{self._extension}' for filename '{self._filename}'"
            )

    @property
    def extension(self):
        return self._extension
