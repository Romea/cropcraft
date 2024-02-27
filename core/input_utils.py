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

import appdirs
import yaml
import json
import os


def generate_safe_dict():
    import math

    safe_list = [
        'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs',
        'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians',
        'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau'
    ]

    safe_dict = dict([(k, getattr(math, k)) for k in safe_list])
    safe_dict['abs'] = abs
    safe_dict['min'] = min
    safe_dict['max'] = max

    return safe_dict


safe_eval_dict = generate_safe_dict()


def safe_eval_fn(variable: str, expression: str):
    return eval(f"lambda {variable}: {expression}", safe_eval_dict)


def user_data_dir():
    return appdirs.user_data_dir(appname='cropcraft')


def load_config_file(basename: str, path='.'):
    yaml_filename = os.path.join(path, basename + '.yaml')
    if os.access(yaml_filename, os.R_OK):
        with open(yaml_filename, 'r') as file:
            return yaml.safe_load(file)

    json_filename = os.path.join(path, basename + '.json')
    if os.access(json_filename, os.R_OK):
        with open(json_filename, 'r') as file:
            return json.load(file)
