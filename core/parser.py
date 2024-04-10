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

import sys
import yaml
import os

from . import config
from . import output as output_classes
from . import input_utils


class ParserError(Exception):
    pass


def make_swath(name: str, data: dict, default=config.Swath(), allow_none=False):
    swath = config.Swath()
    swath.name = name

    def get_element(field, default):
        value = data.get(field, default)
        if not allow_none and value is None:
            raise ParserError(f"Missing element '{field}' and no default value")
        return value

    swath.plant_type = get_element('plant_type', default.plant_type)
    swath.plant_height = get_element('plant_height', default.plant_height)
    swath.plant_distance = get_element('plant_distance', default.plant_distance)
    swath.row_distance = get_element('row_distance', default.row_distance)
    swath.plants_count = get_element('plants_count', default.plants_count)
    swath.rows_count = get_element('rows_count', default.rows_count)
    swath.swaths_count = get_element('swaths_count', default.swaths_count)
    swath.swath_width = get_element('swath_width', default.swath_width)
    swath.shift_next_swath = get_element('shift_next_swath', default.shift_next_swath)
    swath.offset = get_element('offset', default.offset)
    swath.orientation = get_element('orientation', default.orientation)

    if swath.orientation not in ['random', 'aligned', 'zero']:
        raise ParserError(f"The value '{swath.orientation}' is invalid for {name}.orientation")

    y_fn_expr = data.get('y_function')
    if y_fn_expr is not None:
        swath.y_function = input_utils.safe_eval_fn('x', y_fn_expr)
    else:
        swath.y_function = default.y_function

    return swath


def make_noise(data: dict):
    noise = config.Noise()
    noise_data = data.get('noise')
    if noise_data is None:
        return noise

    noise.position = noise_data.get('position', noise.position)
    noise.tilt = noise_data.get('tilt', noise.tilt)
    noise.missing = noise_data.get('missing', noise.missing)
    noise.scale = noise_data.get('scale', noise.scale)
    return noise


def make_weed(name: str, data: dict, cfg_dir: str):
    weed = config.Weed()
    weed.name = name
    weed.plant_type = data.get('plant_type')
    if weed.plant_type is None:
        raise ParserError(f"Missing element 'plant_type' as children of '{name}'")

    weed.density = data.get('density', weed.density)
    weed.distance_min = data.get('distance_min', weed.distance_min)

    weed.scattering_mode = data.get('scattering_mode', weed.scattering_mode)
    if weed.scattering_mode not in ('noise', 'image'): 
        raise ParserError(f"Invalid '{name}.scattering_mode': options are 'noise' or 'image'")

    weed.noise_scale = data.get('noise_scale', weed.noise_scale)
    weed.noise_offset = data.get('noise_offset', weed.noise_offset)
    if weed.noise_offset < -1. or weed.noise_offset > 1.:
        raise ParserError(f"The '{name}.noise_offset' value must be between -1. and 1.")

    if weed.scattering_mode == 'image':
        weed.scattering_img = data.get('scattering_img', weed.scattering_img)
        if weed.scattering_img is not None:
            weed.scattering_img = os.path.join(cfg_dir, weed.scattering_img)
        else:
            raise ParserError(f"'{name}.scattering_img' is necessary in 'image' scatttering mode")

    return weed


def make_stones(field: dict):
    data = field.get('stones')
    if data is None:
        return None

    stones = config.Stones()
    stones.density = data.get('density', stones.density)
    stones.distance_min = data.get('distance_min', stones.distance_min)
    stones.noise_scale = data.get('noise_scale', stones.noise_scale)
    stones.noise_offset = data.get('noise_offset', stones.noise_offset)
    if stones.noise_offset < -1. or stones.noise_offset > 1.:
        raise ParserError("The 'stones.noise_offset' value must be between -1. and 1.")
    return stones


def make_field(cfg: dict, cfg_dir: str):
    field_data = cfg.get('field')
    if field_data is None:
        raise ParserError("Missing element 'field' as root element")

    field = config.Field()
    field.default = make_swath('default', field_data, allow_none=True)
    field.noise = make_noise(field_data)

    swaths_data = field_data.get('swaths')
    if swaths_data is None:
        raise ParserError("Missing element 'swaths' as children of 'field'")

    field.swaths = [make_swath(name, data, field.default) for name, data in swaths_data.items()]

    weeds_data = field_data.get('weeds')
    if weeds_data is not None:
        field.weeds = [make_weed(name, data, cfg_dir) for name, data in weeds_data.items()]

    field.stones = make_stones(field_data)

    field.headland_width = field_data.get('headland_width', field.headland_width)
    field.scattering_extra_width = field_data.get('scattering_extra_width',
                                                  field.scattering_extra_width)
    field.seed = field_data.get('random_seed')

    return field


def make_blender_file(name: str, data: dict):
    output = output_classes.BlenderFile()
    output.type = type
    output.filename = data.get('filename')
    if output.filename is None:
        raise ParserError("Missing element 'filename' in output config '{name}'")
    return output


def make_gazebo_model(name: str, data: dict):
    output = output_classes.GazeboModel()
    output.type = type
    output.name = data.get('name')
    if output.name is None:
        raise ParserError("Missing element 'name' in output config '{name}'")
    output.path = data.get('dirname', output.name.replace(' ', '_'))
    output.author = data.get('author', 'generated by cropcraft')
    output.use_absolute_path = data.get('use_absolute_path', False)
    return output


output_builders = {
    'blender_file': make_blender_file,
    'gazebo_model': make_gazebo_model,
}


def make_output(name: str, data: dict):
    type = data.get('type')
    if type is None:
        raise ParserError(f"Missing field 'type' in output '{name}'")

    builder = output_builders.get(type)
    if builder is None:
        raise ParserError(f"Unknown output type '{type}'")

    return builder(name, data)


def make_outputs(cfg: dict):
    output_data = cfg.get('output')
    if output_data is None:
        raise ParserError("Missing field 'output' as children of the root element")

    output_enabled = cfg.get('output_enabled')
    if output_enabled is None:
        output_enabled = list(output_data.keys())

    outputs = []
    for name in output_enabled:
        output_config = output_data.get(name)
        if output_config is None:
            print(f"Warning: Unknown output config '{name}', skipped", file=sys.stderr)
        else:
            outputs.append(make_output(name, output_config))

    return outputs


def load_yaml_config(filename: str):
    with open(filename, 'r') as file:
        cfg_data = yaml.safe_load(file.read())
    
    cfg = config.Config()
    cfg.field = make_field(cfg_data, os.path.dirname(filename))
    cfg.outputs = make_outputs(cfg_data)

    return cfg
