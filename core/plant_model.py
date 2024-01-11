from dataclasses import dataclass


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
    models: list

    def __hash__(self):
        return hash((self.type, self.name))

    def full_name(self):
        return f"{self.type}_{self.name}"



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
