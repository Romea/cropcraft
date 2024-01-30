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


@dataclass
class Stones:
    density: float = 5.


@dataclass
class Field:
    headland_width: float = 4.
    scattering_extra_width: float = 1.

    default: Swath = None
    noise: Noise = None
    swaths: typing.List[Swath] = None
    weeds: typing.List[Weed] = field(default_factory=lambda: [])
    stones: Stones = None


@dataclass
class Config:
    outputs: list = None
    field: Field = None
