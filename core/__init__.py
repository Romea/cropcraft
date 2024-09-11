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

from importlib.util import find_spec as _find_spec
import subprocess as _subprocess
import sys as _sys


def _install_pkg(package):
    _subprocess.check_call(
        [_sys.executable,  '-m', 'pip', '--disable-pip-version-check', 'install', package]
    )


if not _find_spec('appdirs'):
    _install_pkg('appdirs')
    _reload_site = True

if not _find_spec('yaml'):
    _install_pkg('pyyaml')
    _reload_site = True

if not _find_spec('msgpack'):
    _install_pkg('msgpack')
    _reload_site = True

# refresh sys.path
if _reload_site:
    import site
    from importlib import reload

    reload(site)

from . import base
from . import beds
from . import ground
from . import plant_manager
from . import output
from . import parser
