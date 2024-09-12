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
    width: float = 0.
    leaf_area: float = 0.

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

        model_list = []
        for model_data in description['models']:
            model = PlantModel(
                filename=model_data['filename'],
                height=model_data.get('height'),
                width=model_data.get('width', 0.),
                leaf_area=model_data.get('leaf_area', 0.),
            )
            model.filepath = os.path.join(plant_dir.path, model.filename)
            model_list.append(model)
        self.plant_groups[plant_type] = model_list

    def get_model_list_by_height(self, type: str, height: float, tolerance_coeff) -> typing.List[PlantModel]:
        if type not in self.plant_groups:
            return None

        model_list = self.plant_groups[type]

        lower_bound = (1 - tolerance_coeff) * height
        higher_bound = (1 + tolerance_coeff) * height

        correct_models = [model for model in model_list if model.height >= lower_bound and model.height <= higher_bound]
        return correct_models if correct_models else None
