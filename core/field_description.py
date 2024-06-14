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

from dataclasses import is_dataclass, asdict
import json

from . import config


class DataEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, config.Field):
            return o.as_dict()
        if isinstance(o, config.Swath):
            return o.as_dict()
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


class FieldDescription:
    def __init__(self, field: config.Field):
        self.field = field

    def dump(self, filename: str):
        data = {
            "config": self.field,
            'field': self.field.state,
        }
        with open(filename, "w") as file:
            json.dump(data, file, cls=DataEncoder)
