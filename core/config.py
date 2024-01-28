from dataclasses import dataclass, field
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
    shift_next_bed: bool = None
    offset: typing.List[float] = field(default_factory=lambda: [0., 0., 0.])


@dataclass
class Noise:
    position: float = None
    tilt: float = None
    missing: float = None
    scale: float = None


@dataclass
class Weed:
    name: str = None
    plant_type: str = None
    density: float = None


@dataclass
class Stones:
    density: float = None


@dataclass
class Field:
    headland_width: float = 4.
    scattering_extra_width: float = 1.

    default: Bed = None
    noise: Noise = None
    beds: typing.List[Bed] = None
    weeds: typing.List[Weed] = None
    stones: Stones = None


@dataclass
class Config:
    outputs: list = None
    field: Field = None
