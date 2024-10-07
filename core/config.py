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

from dataclasses import dataclass, field, asdict
import typing


@dataclass
class Bed:
    name: str = None
    plant_type: str = None
    plant_height: float = None
    plant_distance: float = None
    bed_width: float = None
    row_distance: float = None
    plants_count: int = None
    rows_count: int = 1
    beds_count: int = 1
    length: float = None
    shift_next_bed: bool = True
    offset: typing.List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    y_function: typing.Callable[float, float] = lambda x: 0.0
    orientation: str = "random"

    def as_dict(self):
        data = asdict(self)
        data.pop('y_function')
        return data


@dataclass
class Noise:
    position: float = 0.0
    tilt: float = 0.0
    missing: float = 0.0
    scale: float = 0.0


@dataclass
class Weed:
    name: str = None
    plant_type: str = None
    density: float = 5.0
    distance_min: float = 0.12
    scattering_mode: str = "noise"
    noise_scale: float = 0.36
    noise_offset: float = 0.1
    scattering_img: str = None


@dataclass
class Stones:
    density: float = 50.0
    distance_min: float = 0.04
    noise_scale: float = 0.36
    noise_offset: float = 0.23


@dataclass
class PlantState:
    x: float = 0
    y: float = 0
    z: float = 0
    roll: float = 0
    pitch: float = 0
    yaw: float = 0
    height: float = 0
    width: float = 0
    leaf_area: float = 0
    type: str = None
    filename: str = None

@dataclass
class RowState:
    crops: typing.List[PlantState] = field(default_factory=lambda: [])
    leaf_area: float = 0


@dataclass
class BedState:
    rows: typing.List[RowState] = field(default_factory=lambda: [])
    leaf_area: float = 0


@dataclass
class FieldState:
    beds: typing.List[BedState] = field(default_factory=lambda: [])
    leaf_area: float = 0


@dataclass
class Field:
    headland_width: float = 4.0
    scattering_extra_width: float = 1.0
    seed: int = None

    default: Bed = None
    noise: Noise = None
    beds: typing.List[Bed] = None
    weeds: typing.List[Weed] = field(default_factory=lambda: [])
    stones: Stones = None

    state: FieldState = None

    def as_dict(self):
        data = asdict(self)
        data.pop('default')
        data.pop('state')
        data['beds'] = [bed.as_dict() for bed in self.beds]
        return data


@dataclass
class Config:
    outputs: list = None
    field: Field = None
