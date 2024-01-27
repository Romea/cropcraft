from dataclasses import dataclass
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
    rows_count: int = None
    beds_count: int = None
    shift_next_bed: bool = None


@dataclass
class Noise:
    position: float = None
    tilt: float = None
    missing: float = None
    scale: float = None


@dataclass
class Weed:
    plant_type: str = None
    density: float = None


@dataclass
class Stones:
    density: float = None


@dataclass
class Field:
    default: Bed = None
    noise: Noise = None
    beds: typing.List[Bed] = None
    weeds: typing.List[Weed] = None
    stones: Stones = None


@dataclass
class Config:
    outputs: list = None
    field: Field = None
