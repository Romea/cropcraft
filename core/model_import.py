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
        sys.stdout = os.fdopen(fd_out, "w")
        sys.stderr = os.fdopen(fd_err, "w")

    old_out = os.fdopen(os.dup(fd_out), "w")
    old_err = os.fdopen(os.dup(fd_err), "w")

    with open(os.devnull, "w") as file:
        redirect_all(file, file)
    try:
        yield
    finally:
        redirect_all(old_out, old_err)

    old_out.close()
    old_err.close()


def obj_import(filepath: str):
    objects_before = set(bpy.context.scene.objects)

    with disable_outputs():
        bpy.ops.wm.obj_import(
            filepath=filepath,
            up_axis="Z",
            forward_axis="Y",
            use_split_objects=False,
        )

    imported_objects = set(bpy.context.scene.objects) - objects_before
    for object in imported_objects:
        make_transparent(object)



def make_transparent(obj: bpy.types.Object):
    """
    This function modifies the given Blender object to make its material
    transparent by linking the alpha output of its image texture node
    to the alpha input of its Principled BSDF shader node.

    Parameters:
    obj (bpy.types.Object): The Blender object to be modified.
                            It should be of type 'MESH' and have a
                            material with a node tree containing both
                            a Principled BSDF node and an image texture node.
    """
    if obj.type != "MESH":
        return

    material = obj.active_material
    if material is None or material.node_tree is None:
        return

    nodes = material.node_tree.nodes

    bsdf_node = next((node for node in nodes if node.type == "BSDF_PRINCIPLED"), None)
    image_node = next((node for node in nodes if node.type == "TEX_IMAGE"), None)

    if bsdf_node and image_node:
        # create a link from the image node's alpha output to the BSDF's alpha input
        links = material.node_tree.links

        links.new(image_node.outputs["Alpha"], bsdf_node.inputs["Alpha"])
