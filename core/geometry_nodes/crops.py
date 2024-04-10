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

# initialize crops node group
def crops_node_group():
    crops = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "crops")

    crops.is_modifier = True
    
    # initialize crops nodes
    # crops interface
    # Socket Geometry
    geometry_socket = crops.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    
    # Socket Geometry
    geometry_socket_1 = crops.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    
    # Socket Collection
    collection_socket = crops.interface.new_socket(name = "Collection", in_out='INPUT', socket_type = 'NodeSocketCollection')
    collection_socket.attribute_domain = 'POINT'
    
    
    # node Instance on Points
    instance_on_points = crops.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = True
    
    # node Named Attribute
    named_attribute = crops.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT'
    # Name
    named_attribute.inputs[0].default_value = "scale"
    
    # node Named Attribute.001
    named_attribute_001 = crops.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.data_type = 'FLOAT_VECTOR'
    # Name
    named_attribute_001.inputs[0].default_value = "rotation"
    
    # node Collection Info
    collection_info = crops.nodes.new("GeometryNodeCollectionInfo")
    collection_info.name = "Collection Info"
    collection_info.transform_space = 'ORIGINAL'
    # Separate Children
    collection_info.inputs[1].default_value = True
    # Reset Children
    collection_info.inputs[2].default_value = True
    
    # node Group Input
    group_input = crops.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    
    # node Reroute
    reroute = crops.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    # node Realize Instances
    realize_instances = crops.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    
    # node Group Output
    group_output = crops.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    
    # node Named Attribute.002
    named_attribute_002 = crops.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.data_type = 'INT'
    # Name
    named_attribute_002.inputs[0].default_value = "index"
    
    
    
    
    # Set locations
    instance_on_points.location = (111.75765991210938, 2.6148529052734375)
    named_attribute.location = (-82.4139404296875, -210.76528930664062)
    named_attribute_001.location = (-233.90682983398438, -167.69667053222656)
    collection_info.location = (-71.25875091552734, 10.484445571899414)
    group_input.location = (-237.2997589111328, 57.182106018066406)
    reroute.location = (72.57816314697266, 22.990873336791992)
    realize_instances.location = (274.9822082519531, 28.737092971801758)
    group_output.location = (443.89154052734375, 30.682458877563477)
    named_attribute_002.location = (-390.4229736328125, -124.10218811035156)
    
    # Set dimensions
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    named_attribute.width, named_attribute.height = 140.0, 100.0
    named_attribute_001.width, named_attribute_001.height = 140.0, 100.0
    collection_info.width, collection_info.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    reroute.width, reroute.height = 16.0, 100.0
    realize_instances.width, realize_instances.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    named_attribute_002.width, named_attribute_002.height = 140.0, 100.0
    
    # initialize crops links
    # collection_info.Instances -> instance_on_points.Instance
    crops.links.new(collection_info.outputs[0], instance_on_points.inputs[2])
    # group_input.Collection -> collection_info.Collection
    crops.links.new(group_input.outputs[1], collection_info.inputs[0])
    # instance_on_points.Instances -> realize_instances.Geometry
    crops.links.new(instance_on_points.outputs[0], realize_instances.inputs[0])
    # named_attribute_001.Attribute -> instance_on_points.Rotation
    crops.links.new(named_attribute_001.outputs[0], instance_on_points.inputs[5])
    # reroute.Output -> instance_on_points.Points
    crops.links.new(reroute.outputs[0], instance_on_points.inputs[0])
    # named_attribute_002.Attribute -> instance_on_points.Instance Index
    crops.links.new(named_attribute_002.outputs[0], instance_on_points.inputs[4])
    # group_input.Geometry -> reroute.Input
    crops.links.new(group_input.outputs[0], reroute.inputs[0])
    # instance_on_points.Instances -> group_output.Geometry
    crops.links.new(instance_on_points.outputs[0], group_output.inputs[0])
    # named_attribute.Attribute -> instance_on_points.Scale
    crops.links.new(named_attribute.outputs[0], instance_on_points.inputs[6])
    return crops
