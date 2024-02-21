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

import bpy
from contextlib import contextmanager
import os
import sys


@contextmanager
def disable_outputs():
    fd_out = sys.stdout.fileno()
    fd_err = sys.stderr.fileno()

    def redirect_all(out, err):
        sys.stdout.close()
        sys.stderr.close()
        os.dup2(out.fileno(), fd_out)
        os.dup2(err.fileno(), fd_err)
        sys.stdout = os.fdopen(fd_out, 'w')
        sys.stderr = os.fdopen(fd_err, 'w')

    old_out = os.fdopen(os.dup(fd_out), 'w')
    old_err = os.fdopen(os.dup(fd_err), 'w')

    with open(os.devnull, 'w') as file:
        redirect_all(file, file)
    try:
        yield
    finally:
        redirect_all(old_out, old_err)

    old_out.close()
    old_err.close()


def obj_import(filepath: str):
    with disable_outputs():
        bpy.ops.wm.obj_import(
            filepath=filepath,
            up_axis='Z',
            forward_axis='Y',
            use_split_objects=False,
        )
