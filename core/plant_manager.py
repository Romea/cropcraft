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

from dataclasses import dataclass, field
import typing
import os

from . import input_utils


@dataclass
class PlantModel:
    filename: str
    height: float
    filepath: str = None
    width: float = None
    leaf_area: float = None


@dataclass
class PlantGroup:
    type: str
    name: str
    min_height: float
    models: typing.List[PlantModel] = field(default_factory=lambda: [])

    def __hash__(self):
        return hash((self.type, self.name))

    def full_name(self):
        return f"{self.type}_{self.name}"

    def average_height(self):
        sum = 0.
        for model in self.models:
            sum += model.height
        return sum / len(self.models) if len(self.models) else self.min_height

    def append(self, model: PlantModel):
        self.models.append(model)


@dataclass
class Plant:
    x: float = 0.
    y: float = 0.
    radius: float = 0.
    height: float = 0.


class PlantManager:

    def __init__(self):
        self.plant_groups = {}
        self.load_plants(os.path.abspath('assets/plants'))

        user_plants_dir = os.path.join(input_utils.user_data_dir(), 'plants')
        if os.path.isdir(user_plants_dir):
            self.load_plants(user_plants_dir)

    def load_plants(self, dirname: str):
        if not os.access(dirname, os.R_OK):
            return

        for plant_dir in os.scandir(dirname):
            data = input_utils.load_config_file('description', plant_dir.path)
            if data is not None:
                self.update_groups(plant_dir, data)

    def update_groups(self, plant_dir: os.DirEntry, description: dict):
        plant_type = plant_dir.name

        if plant_type not in self.plant_groups:
            self.plant_groups[plant_type] = {}

        groups = self.plant_groups[plant_type]

        for group_name, group_data in description['model_groups'].items():
            group = PlantGroup(
                type=plant_type,
                name=group_name,
                min_height=group_data['minimal_height'],
            )
            for model_data in group_data['models']:
                model = PlantModel(
                    filename=model_data['filename'],
                    height=model_data.get('height'),
                    width=model_data.get('width'),
                    leaf_area=model_data.get('leaf_area'),
                )
                model.filepath = os.path.join(plant_dir.path, model.filename)
                group.append(model)

            if group_name in groups:
                groups[group_name].models += group.models
            else:
                groups[group_name] = group

    def get_group_by_height(self, type: str, height: float):
        if type not in self.plant_groups:
            return None

        groups = self.plant_groups[type]

        group = None
        for cur_group in groups.values():
            if cur_group.min_height > height:
                break
            group = cur_group

        return group
