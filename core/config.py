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

@dataclass
class Swath:
    name: str = None
    plant_type: str = None
    plant_height: float = None
    plant_distance: float = None
    swath_width: float = None
    row_distance: float = None
    plants_count: int = None
    rows_count: int = 1
    swaths_count: int = 1
    shift_next_swath: bool = True
    offset: typing.List[float] = field(default_factory=lambda: [0., 0., 0.])
    y_function: typing.Callable[float, float] = lambda x: 0.
    orientation: str = 'random'


@dataclass
class Noise:
    position: float = 0.
    tilt: float = 0.
    missing: float = 0.
    scale: float = 0.


@dataclass
class Weed:
    name: str = None
    plant_type: str = None
    density: float = 5.
    distance_min: float = 0.12
    scattering_mode: str='noise'
    noise_scale: float = 0.36
    noise_offset: float = 0.1
    scattering_img: str = None


@dataclass
class Stones:
    density: float = 50.
    distance_min: float = 0.04
    noise_scale: float = 0.36
    noise_offset: float = 0.23


@dataclass
class Field:
    headland_width: float = 4.
    scattering_extra_width: float = 1.
    seed: int = None

    default: Swath = None
    noise: Noise = None
    swaths: typing.List[Swath] = None
    weeds: typing.List[Weed] = field(default_factory=lambda: [])
    stones: Stones = None


@dataclass
class Config:
    outputs: list = None
    field: Field = None
