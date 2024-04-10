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

# initialize scattering node group
def scattering_from_image_node_group():
	scattering = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "scattering_from_image")

	scattering.is_modifier = True
	
	# initialize scattering nodes
	# scattering interface
	# Socket Geometry
	geometry_socket = scattering.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
	geometry_socket.attribute_domain = 'POINT'
	
	# Socket Geometry
	geometry_socket_1 = scattering.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
	geometry_socket_1.attribute_domain = 'POINT'
	
	# Socket Density Factor
	density_factor_socket = scattering.interface.new_socket(name = "Density Factor", in_out='INPUT', socket_type = 'NodeSocketFloat')
	density_factor_socket.subtype = 'FACTOR'
	density_factor_socket.default_value = 1.0
	density_factor_socket.min_value = 0.0
	density_factor_socket.max_value = 1.0
	density_factor_socket.attribute_domain = 'POINT'
	
	# Socket Collection
	collection_socket = scattering.interface.new_socket(name = "Collection", in_out='INPUT', socket_type = 'NodeSocketCollection')
	collection_socket.attribute_domain = 'POINT'
	
	# Socket Seed
	seed_socket = scattering.interface.new_socket(name = "Seed", in_out='INPUT', socket_type = 'NodeSocketInt')
	seed_socket.subtype = 'NONE'
	seed_socket.default_value = 15
	seed_socket.min_value = -2147483648
	seed_socket.max_value = 2147483647
	seed_socket.attribute_domain = 'POINT'
	
	# Socket Distance Min
	distance_min_socket = scattering.interface.new_socket(name = "Distance Min", in_out='INPUT', socket_type = 'NodeSocketFloat')
	distance_min_socket.subtype = 'DISTANCE'
	distance_min_socket.default_value = 0.11999999731779099
	distance_min_socket.min_value = 0.0
	distance_min_socket.max_value = 3.4028234663852886e+38
	distance_min_socket.attribute_domain = 'POINT'
	
	# Socket Density
	density_socket = scattering.interface.new_socket(name = "Density", in_out='INPUT', socket_type = 'NodeSocketFloat')
	density_socket.subtype = 'NONE'
	density_socket.default_value = 5.0
	density_socket.min_value = 0.0
	density_socket.max_value = 1000.0
	density_socket.attribute_domain = 'POINT'
	
	# Socket Noise Scale
	noise_scale_socket = scattering.interface.new_socket(name = "Noise Scale", in_out='INPUT', socket_type = 'NodeSocketFloat')
	noise_scale_socket.subtype = 'NONE'
	noise_scale_socket.default_value = 0.36000001430511475
	noise_scale_socket.min_value = 0.0
	noise_scale_socket.max_value = 3.4028234663852886e+38
	noise_scale_socket.attribute_domain = 'POINT'
	
	# Socket Noise Offset
	noise_offset_socket = scattering.interface.new_socket(name = "Noise Offset", in_out='INPUT', socket_type = 'NodeSocketFloat')
	noise_offset_socket.subtype = 'NONE'
	noise_offset_socket.default_value = 0.10000000149011612
	noise_offset_socket.min_value = -1.0
	noise_offset_socket.max_value = 1.0
	noise_offset_socket.attribute_domain = 'POINT'
	
	# Socket Image
	image_socket = scattering.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketImage')
	image_socket.attribute_domain = 'POINT'
	
	
	# node Random Value.001
	random_value_001 = scattering.nodes.new("FunctionNodeRandomValue")
	random_value_001.name = "Random Value.001"
	random_value_001.data_type = 'FLOAT'
	# Min
	random_value_001.inputs[0].default_value = (0.0, 0.0, 0.0)
	# Max
	random_value_001.inputs[1].default_value = (0.0, 0.0, 6.283199787139893)
	# Min_001
	random_value_001.inputs[2].default_value = 0.699999988079071
	# Max_001
	random_value_001.inputs[3].default_value = 1.0
	# Min_002
	random_value_001.inputs[4].default_value = 0
	# Max_002
	random_value_001.inputs[5].default_value = 100
	# Probability
	random_value_001.inputs[6].default_value = 0.5
	# ID
	random_value_001.inputs[7].default_value = 0
	
	# node Collection Info
	collection_info = scattering.nodes.new("GeometryNodeCollectionInfo")
	collection_info.name = "Collection Info"
	collection_info.transform_space = 'ORIGINAL'
	# Separate Children
	collection_info.inputs[1].default_value = True
	# Reset Children
	collection_info.inputs[2].default_value = True
	
	# node Random Value
	random_value = scattering.nodes.new("FunctionNodeRandomValue")
	random_value.name = "Random Value"
	random_value.data_type = 'FLOAT_VECTOR'
	# Min
	random_value.inputs[0].default_value = (-0.10000000149011612, -0.10000000149011612, 0.0)
	# Max
	random_value.inputs[1].default_value = (0.10000000149011612, 0.10000000149011612, 6.283199787139893)
	# Min_001
	random_value.inputs[2].default_value = 0.0
	# Max_001
	random_value.inputs[3].default_value = 1.0
	# Min_002
	random_value.inputs[4].default_value = 0
	# Max_002
	random_value.inputs[5].default_value = 100
	# Probability
	random_value.inputs[6].default_value = 0.5
	# ID
	random_value.inputs[7].default_value = 0
	
	# node Realize Instances
	realize_instances = scattering.nodes.new("GeometryNodeRealizeInstances")
	realize_instances.name = "Realize Instances"
	
	# node Group Output
	group_output = scattering.nodes.new("NodeGroupOutput")
	group_output.name = "Group Output"
	group_output.is_active_output = True
	
	# node Instance on Points
	instance_on_points = scattering.nodes.new("GeometryNodeInstanceOnPoints")
	instance_on_points.name = "Instance on Points"
	# Selection
	instance_on_points.inputs[1].default_value = True
	# Pick Instance
	instance_on_points.inputs[3].default_value = True
	# Instance Index
	instance_on_points.inputs[4].default_value = 0
	
	# node Group Input.001
	group_input_001 = scattering.nodes.new("NodeGroupInput")
	group_input_001.name = "Group Input.001"
	
	# node Distribute Points on Faces
	distribute_points_on_faces = scattering.nodes.new("GeometryNodeDistributePointsOnFaces")
	distribute_points_on_faces.name = "Distribute Points on Faces"
	distribute_points_on_faces.distribute_method = 'POISSON'
	distribute_points_on_faces.use_legacy_normal = True
	# Selection
	distribute_points_on_faces.inputs[1].default_value = True
	
	# node Group Input
	group_input = scattering.nodes.new("NodeGroupInput")
	group_input.name = "Group Input"
	
	# node Image Texture
	image_texture = scattering.nodes.new("GeometryNodeImageTexture")
	image_texture.name = "Image Texture"
	image_texture.extension = 'REPEAT'
	image_texture.interpolation = 'Linear'
	# Frame
	image_texture.inputs[2].default_value = 0
	
	# node Position
	position = scattering.nodes.new("GeometryNodeInputPosition")
	position.name = "Position"
	
	# node Map Range
	map_range = scattering.nodes.new("ShaderNodeMapRange")
	map_range.name = "Map Range"
	map_range.clamp = True
	map_range.data_type = 'FLOAT_VECTOR'
	map_range.interpolation_type = 'LINEAR'
	# To Min
	map_range.inputs[3].default_value = 0.0
	# To Max
	map_range.inputs[4].default_value = 1.0
	# Steps
	map_range.inputs[5].default_value = 4.0
	# To_Min_FLOAT3
	map_range.inputs[9].default_value = (0.0, 0.0, 0.0)
	# To_Max_FLOAT3
	map_range.inputs[10].default_value = (1.0, 1.0, 1.0)
	# Steps_FLOAT3
	map_range.inputs[11].default_value = (4.0, 4.0, 4.0)
	
	# node Bounding Box
	bounding_box = scattering.nodes.new("GeometryNodeBoundBox")
	bounding_box.name = "Bounding Box"
	
	# node Group Input.002
	group_input_002 = scattering.nodes.new("NodeGroupInput")
	group_input_002.name = "Group Input.002"
	
	
	
	
	# Set locations
	random_value_001.location = (155.633056640625, -179.60244750976562)
	collection_info.location = (-23.232402801513672, 39.906593322753906)
	random_value.location = (-27.310951232910156, -123.05940246582031)
	realize_instances.location = (507.9872741699219, 34.4013786315918)
	group_output.location = (742.9833984375, 33.78972244262695)
	instance_on_points.location = (323.0923156738281, 9.463346481323242)
	group_input_001.location = (-245.5984344482422, -142.40048217773438)
	distribute_points_on_faces.location = (-244.30825805664062, 258.3542785644531)
	group_input.location = (-446.5732727050781, 229.36117553710938)
	image_texture.location = (-566.1689453125, -50.892486572265625)
	position.location = (-985.07958984375, -63.980403900146484)
	map_range.location = (-762.05029296875, 27.360782623291016)
	bounding_box.location = (-978.46630859375, -139.85723876953125)
	group_input_002.location = (-1178.828369140625, -131.23370361328125)
	
	# Set dimensions
	random_value_001.width, random_value_001.height = 140.0, 100.0
	collection_info.width, collection_info.height = 140.0, 100.0
	random_value.width, random_value.height = 140.0, 100.0
	realize_instances.width, realize_instances.height = 140.0, 100.0
	group_output.width, group_output.height = 140.0, 100.0
	instance_on_points.width, instance_on_points.height = 140.0, 100.0
	group_input_001.width, group_input_001.height = 140.0, 100.0
	distribute_points_on_faces.width, distribute_points_on_faces.height = 170.0, 100.0
	group_input.width, group_input.height = 140.0, 100.0
	image_texture.width, image_texture.height = 240.0, 100.0
	position.width, position.height = 140.0, 100.0
	map_range.width, map_range.height = 140.0, 100.0
	bounding_box.width, bounding_box.height = 140.0, 100.0
	group_input_002.width, group_input_002.height = 140.0, 100.0
	
	# initialize scattering links
	# distribute_points_on_faces.Points -> instance_on_points.Points
	scattering.links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])
	# collection_info.Instances -> instance_on_points.Instance
	scattering.links.new(collection_info.outputs[0], instance_on_points.inputs[2])
	# random_value.Value -> instance_on_points.Rotation
	scattering.links.new(random_value.outputs[0], instance_on_points.inputs[5])
	# random_value_001.Value -> instance_on_points.Scale
	scattering.links.new(random_value_001.outputs[1], instance_on_points.inputs[6])
	# group_input.Seed -> distribute_points_on_faces.Seed
	scattering.links.new(group_input.outputs[3], distribute_points_on_faces.inputs[6])
	# group_input.Geometry -> distribute_points_on_faces.Mesh
	scattering.links.new(group_input.outputs[0], distribute_points_on_faces.inputs[0])
	# instance_on_points.Instances -> realize_instances.Geometry
	scattering.links.new(instance_on_points.outputs[0], realize_instances.inputs[0])
	# group_input_001.Collection -> collection_info.Collection
	scattering.links.new(group_input_001.outputs[2], collection_info.inputs[0])
	# group_input_001.Seed -> random_value_001.Seed
	scattering.links.new(group_input_001.outputs[3], random_value_001.inputs[8])
	# group_input_001.Seed -> random_value.Seed
	scattering.links.new(group_input_001.outputs[3], random_value.inputs[8])
	# group_input.Density -> distribute_points_on_faces.Density Max
	scattering.links.new(group_input.outputs[5], distribute_points_on_faces.inputs[3])
	# image_texture.Color -> distribute_points_on_faces.Density
	scattering.links.new(image_texture.outputs[0], distribute_points_on_faces.inputs[4])
	# bounding_box.Min -> map_range.From Min
	scattering.links.new(bounding_box.outputs[1], map_range.inputs[1])
	# bounding_box.Max -> map_range.From Max
	scattering.links.new(bounding_box.outputs[2], map_range.inputs[2])
	# image_texture.Color -> distribute_points_on_faces.Density Factor
	scattering.links.new(image_texture.outputs[0], distribute_points_on_faces.inputs[5])
	# group_input.Distance Min -> distribute_points_on_faces.Distance Min
	scattering.links.new(group_input.outputs[4], distribute_points_on_faces.inputs[2])
	# position.Position -> map_range.Value
	scattering.links.new(position.outputs[0], map_range.inputs[0])
	# bounding_box.Min -> map_range.From Min
	scattering.links.new(bounding_box.outputs[1], map_range.inputs[7])
	# bounding_box.Max -> map_range.From Max
	scattering.links.new(bounding_box.outputs[2], map_range.inputs[8])
	# position.Position -> map_range.Vector
	scattering.links.new(position.outputs[0], map_range.inputs[6])
	# map_range.Vector -> image_texture.Vector
	scattering.links.new(map_range.outputs[1], image_texture.inputs[1])
	# realize_instances.Geometry -> group_output.Geometry
	scattering.links.new(realize_instances.outputs[0], group_output.inputs[0])
	# group_input_002.Geometry -> bounding_box.Geometry
	scattering.links.new(group_input_002.outputs[0], bounding_box.inputs[0])
	# group_input_002.Image -> image_texture.Image
	scattering.links.new(group_input_002.outputs[8], image_texture.inputs[0])
	return scattering
