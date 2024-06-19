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
import msgpack
import gzip

from . import config


class DataEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, config.Field):
            return o.as_dict()
        if isinstance(o, config.Bed):
            return o.as_dict()
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


class FieldDescription:
    def __init__(self, field: config.Field):
        self.field = field
        self.export_fns = {
            'json': self._export_json,
            'messagepack': self._export_mpk,
            'compressed_messagepack': self._export_mpkgz,
        }

    def dump(self, filename: str, format: str = None):
        data = {
            'config': self.field,
            'field': self.field.state,
        }
        if format is None:
            format = self._get_format_from_extension(filename)

        export_fn = self.export_fns.get(format)
        if export_fn is None:
            raise Exception("Unknown export format for the description output of '{filename}'")
        self.export_fns[format](data, filename)

    def _export_json(self, data: dict, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, cls=DataEncoder)

    def _export_mpk(self, data: dict, filename):
        with open(filename, 'wb') as file:
            encoder = DataEncoder()
            msgpack.dump(data, file, default=encoder.default)

    def _export_mpkgz(self, data: dict, filename):
        with gzip.open(filename, 'wb') as file:
            encoder = DataEncoder()
            msgpack.dump(data, file, default=encoder.default)

    def _get_format_from_extension(self, filename: str):
        if filename.endswith('.mpk.gz'):
            return 'compressed_messagepack'
        if filename.endswith('.mpk'):
            return 'messagepack'
        # default to JSON
        return 'json'
