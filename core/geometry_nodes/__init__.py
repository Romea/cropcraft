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

from .crops import crops_node_group
from .scattering_from_image import scattering_from_image_node_group
from .scattering import scattering_node_group
from .stones_scattering import stones_scattering_node_group

def create_all_node_group():
    crops_node_group()
    scattering_node_group()
    stones_scattering_node_group()
    scattering_from_image_node_group()
