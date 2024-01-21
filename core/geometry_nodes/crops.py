import bpy

# initialize crops node group
def crops_node_group():
	crops = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "crops")

	crops.is_modifier = True

	# initialize crops nodes
	# node Instance on Points
	instance_on_points = crops.nodes.new("GeometryNodeInstanceOnPoints")
	instance_on_points.name = "Instance on Points"
	# Selection
	instance_on_points.inputs[1].default_value = True
	# Pick Instance
	instance_on_points.inputs[3].default_value = True
	# Instance Index
	instance_on_points.inputs[4].default_value = 0

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
	# crops inputs
	# input Geometry
	geometry_socket = crops.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
	geometry_socket.attribute_domain = 'POINT'

	# input Collection
	collection_socket = crops.interface.new_socket(name = "Collection", in_out='INPUT', socket_type = 'NodeSocketCollection')
	collection_socket.attribute_domain = 'POINT'


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
	# crops outputs
	# output Geometry
	geometry_socket = crops.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
	geometry_socket.attribute_domain = 'POINT'


	# Set locations
	instance_on_points.location = (111.75765991210938, 2.6148529052734375)
	named_attribute.location = (-65.23535919189453, -183.43814086914062)
	named_attribute_001.location = (-214.72067260742188, -131.24696350097656)
	collection_info.location = (-63.174713134765625, -8.745773315429688)
	group_input.location = (-239.32077026367188, 44.02458572387695)
	reroute.location = (78.6053466796875, 9.833354949951172)
	realize_instances.location = (274.9822082519531, 28.737092971801758)
	group_output.location = (443.89154052734375, 30.682458877563477)

	# Set dimensions
	instance_on_points.width, instance_on_points.height = 140.0, 100.0
	named_attribute.width, named_attribute.height = 140.0, 100.0
	named_attribute_001.width, named_attribute_001.height = 140.0, 100.0
	collection_info.width, collection_info.height = 140.0, 100.0
	group_input.width, group_input.height = 140.0, 100.0
	reroute.width, reroute.height = 16.0, 100.0
	realize_instances.width, realize_instances.height = 140.0, 100.0
	group_output.width, group_output.height = 140.0, 100.0

	# initialize crops links
	# collection_info.Instances -> instance_on_points.Instance
	crops.links.new(collection_info.outputs[0], instance_on_points.inputs[2])
	# group_input.Collection -> collection_info.Collection
	crops.links.new(group_input.outputs[1], collection_info.inputs[0])
	# realize_instances.Geometry -> group_output.Geometry
	crops.links.new(realize_instances.outputs[0], group_output.inputs[0])
	# instance_on_points.Instances -> realize_instances.Geometry
	crops.links.new(instance_on_points.outputs[0], realize_instances.inputs[0])
	# named_attribute.Attribute -> instance_on_points.Scale
	crops.links.new(named_attribute.outputs[1], instance_on_points.inputs[6])
	# named_attribute_001.Attribute -> instance_on_points.Rotation
	crops.links.new(named_attribute_001.outputs[0], instance_on_points.inputs[5])
	# reroute.Output -> instance_on_points.Points
	crops.links.new(reroute.outputs[0], instance_on_points.inputs[0])
	# group_input.Geometry -> reroute.Input
	crops.links.new(group_input.outputs[0], reroute.inputs[0])
	return crops
