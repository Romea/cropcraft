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

_reload_site = False

from importlib.util import find_spec

if not find_spec('appdirs'):
    import pip
    pip.main(['install', 'appdirs', '--user'])
    _reload_site = True

if not find_spec('yaml'):
    import pip
    pip.main(['install', 'pyyaml', '--user'])
    _reload_site = True

# refresh sys.path
if _reload_site:
    import site
    from importlib import reload
    reload(site)

from . import base
from . import swaths
from . import ground
from . import plant_manager
from . import output
from . import parser
