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
import yaml
import json


@dataclass
class PlantModel:
    filename: str
    height: float
    width: float = None
    leaf_area: float = None

    @staticmethod
    def from_dict(data: dict):
        return PlantModel(
            filename=data['filename'],
            height=data['height'],
            width=data.get('width'),
            leaf_area=data.get('leaf_area'),
        )


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
        self.load_plants('assets/plants')

    def load_plants(self, dirname: str):
        for plant_dir in os.scandir(dirname):
            data = self.load_description(plant_dir)
            if data is not None:
                self.update_groups(plant_dir.name, data)

    def load_description(self, dir: os.DirEntry):
        yaml_description_file = os.path.join(dir.path, 'description.yaml')
        if os.access(yaml_description_file, os.R_OK):
            with open(yaml_description_file, 'r') as file:
                return yaml.safe_load(file)

        json_description_file = os.path.join(dir.path, 'description.json')
        if os.access(json_description_file, os.R_OK):
            with open(json_description_file, 'r') as file:
                return json.load(file)

    def update_groups(self, plant_type: str, description: dict):
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
                group.append(PlantModel.from_dict(model_data))

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
