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
import typing


@dataclass
class PlantModel:
    filename: str
    height: float
    radius: float


@dataclass
class PlantGroup:
    type: str
    name: str
    min_height: float
    models: typing.List[PlantModel]

    def __hash__(self):
        return hash((self.type, self.name))

    def full_name(self):
        return f"{self.type}_{self.name}"

    def average_height(self):
        sum = 0.
        for model in self.models:
            sum += model.height
        return sum / len(self.models) if len(self.models) else self.min_height


@dataclass
class Plant:
    x: float = 0.
    y: float = 0.
    radius: float = 0.
    height: float = 0.


plant_groups = {
    'bean': [
        PlantGroup('bean', 'small', .0, [PlantModel('bean_small.obj', .05, .06)]),
        PlantGroup('bean', 'medium', .1, [PlantModel('bean_medium.obj', .135, .11)]),
        PlantGroup('bean', 'big', .2, [PlantModel('bean_big.obj', .217, .16)]),
    ],
    'maize': [
        PlantGroup('maize', 'small', .0, [PlantModel('maize_small.obj', .21, .09)]),
        PlantGroup('maize', 'medium', .24, [PlantModel('maize_medium.obj', .35, .20)]),
        PlantGroup('maize', 'big', .4, [
            PlantModel('maize_big_1.obj', .49, .33),
            PlantModel('maize_big_2.obj', .40, .33),
            PlantModel('maize_big_3.obj', .45, .30),
        ]),
    ],
    'vine1': [
        PlantGroup('vine1', 'medium', .0, [
            PlantModel('vine_01.obj', 1.4, 1.2),
            PlantModel('vine_02.obj', 1.4, 1.2),
            PlantModel('vine_03.obj', 1.4, 1.2),
            PlantModel('vine_04.obj', 1.4, 1.2),
        ]),
    ],
    'vine2': [
        PlantGroup('vine2', 'medium', .0, [
            PlantModel('vine_01.obj', 1.4, 1.2),
        ]),
    ],
}


def get_plant_group(type: str, height: float):
    try:
        model_groups = plant_groups[type]
    except KeyError:
        return None

    group = None
    for cur_group in model_groups:
        if cur_group.min_height > height:
            break
        group = cur_group

    return group
