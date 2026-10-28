# Copyright 2024 INRAE, French National Research Institute for Agriculture, Food and Environment
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

_FLOAT_OFFSETS = {
    'FLOAT_VECTOR': 0,
    'FLOAT': 2,
    'INT': 4,
}


def set_modifier_input(modifier, identifier, value):
    inputs = getattr(getattr(modifier, "properties", None), "inputs", None)
    if inputs is not None and hasattr(inputs, identifier):
        getattr(inputs, identifier).value = value
    else:
        modifier[identifier] = value


def configure_random_value(node, data_type, min_value, max_value,
                           probability=0.5, id_value=0, seed=0):
    node.data_type = data_type

    if len(node.inputs) >= 9:
        offset = _FLOAT_OFFSETS[data_type]
        node.inputs[offset].default_value = min_value
        node.inputs[offset + 1].default_value = max_value
        node.inputs[6].default_value = probability
        node.inputs[7].default_value = id_value
        node.inputs[8].default_value = seed
    else:
        node.inputs["Min"].default_value = min_value
        node.inputs["Max"].default_value = max_value
        node.inputs["ID"].default_value = id_value
        node.inputs["Seed"].default_value = seed

    return node.outputs[1] if data_type == 'FLOAT' and len(node.outputs) > 1 else node.outputs[0]
