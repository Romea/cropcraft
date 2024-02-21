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
import os
import random

this_module_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, this_module_dir)

import core


def configure_random_seed(field: core.config.Field):
    if field.seed is None:
        seed = random.getrandbits(32)
        field.seed = seed

    random.seed(field.seed)


def main(argv: list):
    args = argv[argv.index('--') + 1:]
    config_file = args[0]
    output_dir = args[1]

    try:
        cfg = core.parser.load_yaml_config(config_file)
    except core.parser.ParserError as e:
        print(f"Error: Failed to load config file '{config_file}': {e}", file=sys.stderr)
        exit(1)

    field = cfg.field
    
    configure_random_seed(field)
    core.base.create_blender_context()
    
    swaths = core.swaths.Swaths(field)
    swaths.load_plants()
    swaths.create_swaths()

    ground = core.ground.Ground(field, swaths)
    ground.load_weeds()
    ground.load_stones()
    ground.create_plane()
    ground.create_weeds()
    ground.create_stones()

    look_at = swaths.get_center_pos()
    look_at.x = 5.
    core.base.create_camera(look_at)

    for output in cfg.outputs:
        output.export(output_dir, field)

    print(f'Generated seed: {field.seed}')


if __name__ == '__main__':
    main(sys.argv)
