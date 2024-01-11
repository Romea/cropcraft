import bpy

# initialize crops node group
def crops_node_group():
	crops = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "crops")

	crops.is_modifier = True

	# initialize crops nodes
	# node Frame
	frame = crops.nodes.new("NodeFrame")
	frame.label = "rotation"
	frame.name = "Frame"
	frame.label_size = 20
	frame.shrink = True

	# node Frame.002
	frame_002 = crops.nodes.new("NodeFrame")
	frame_002.label = "scale"
	frame_002.name = "Frame.002"
	frame_002.label_size = 20
	frame_002.shrink = True

	# node Frame.001
	frame_001 = crops.nodes.new("NodeFrame")
	frame_001.label = "translation"
	frame_001.name = "Frame.001"
	frame_001.label_size = 20
	frame_001.shrink = True

	# node Instance on Points
	instance_on_points = crops.nodes.new("GeometryNodeInstanceOnPoints")
	instance_on_points.name = "Instance on Points"
	# Pick Instance
	instance_on_points.inputs[3].default_value = True
	# Instance Index
	instance_on_points.inputs[4].default_value = 0

	# node Random Value.002
	random_value_002 = crops.nodes.new("FunctionNodeRandomValue")
	random_value_002.name = "Random Value.002"
	random_value_002.data_type = 'BOOLEAN'
	# Min
	random_value_002.inputs[0].default_value = (0.0, 0.0, 0.0)
	# Max
	random_value_002.inputs[1].default_value = (1.0, 1.0, 1.0)
	# Min_001
	random_value_002.inputs[2].default_value = 0.0
	# Max_001
	random_value_002.inputs[3].default_value = 1.0
	# Min_002
	random_value_002.inputs[4].default_value = 0
	# Max_002
	random_value_002.inputs[5].default_value = 100
	# ID
	random_value_002.inputs[7].default_value = 0

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

	# input density
	density_socket = crops.interface.new_socket(name = "density", in_out='INPUT', socket_type = 'NodeSocketFloat')
	density_socket.subtype = 'FACTOR'
	density_socket.default_value = 0.9083333015441895
	density_socket.min_value = 0.0
	density_socket.max_value = 1.0
	density_socket.attribute_domain = 'POINT'

	# input Collection
	collection_socket = crops.interface.new_socket(name = "Collection", in_out='INPUT', socket_type = 'NodeSocketCollection')
	collection_socket.attribute_domain = 'POINT'

	# input Seed
	seed_socket = crops.interface.new_socket(name = "Seed", in_out='INPUT', socket_type = 'NodeSocketInt')
	seed_socket.subtype = 'NONE'
	seed_socket.default_value = 0
	seed_socket.min_value = -10000
	seed_socket.max_value = 10000
	seed_socket.attribute_domain = 'POINT'

	# input scale
	scale_socket = crops.interface.new_socket(name = "scale", in_out='INPUT', socket_type = 'NodeSocketFloat')
	scale_socket.subtype = 'NONE'
	scale_socket.default_value = 1.0
	scale_socket.min_value = -10000.0
	scale_socket.max_value = 10000.0
	scale_socket.attribute_domain = 'POINT'



	# node Group Input.001
	group_input_001 = crops.nodes.new("NodeGroupInput")
	group_input_001.name = "Group Input.001"

	# node Vector Math
	vector_math = crops.nodes.new("ShaderNodeVectorMath")
	vector_math.name = "Vector Math"
	vector_math.operation = 'SCALE'
	# Vector_001
	vector_math.inputs[1].default_value = (0.0, 0.0, 0.0)
	# Vector_002
	vector_math.inputs[2].default_value = (0.0, 0.0, 0.0)
	# Scale
	vector_math.inputs[3].default_value = -1.0

	# node Random Value
	random_value = crops.nodes.new("FunctionNodeRandomValue")
	random_value.name = "Random Value"
	random_value.data_type = 'FLOAT_VECTOR'
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

	# node Vector
	vector = crops.nodes.new("FunctionNodeInputVector")
	vector.name = "Vector"
	vector.vector = (0.07000000029802322, 0.07000000029802322, 3.1414999961853027)

	# node Group Input.003
	group_input_003 = crops.nodes.new("NodeGroupInput")
	group_input_003.name = "Group Input.003"

	# node Random Value.001
	random_value_001 = crops.nodes.new("FunctionNodeRandomValue")
	random_value_001.name = "Random Value.001"
	random_value_001.data_type = 'FLOAT'
	# Min
	random_value_001.inputs[0].default_value = (0.0, 0.0, 0.0)
	# Max
	random_value_001.inputs[1].default_value = (1.0, 1.0, 1.0)
	# Min_002
	random_value_001.inputs[4].default_value = 0
	# Max_002
	random_value_001.inputs[5].default_value = 100
	# Probability
	random_value_001.inputs[6].default_value = 0.5
	# ID
	random_value_001.inputs[7].default_value = 0
	# Seed
	random_value_001.inputs[8].default_value = 0

	# node Group Input.004
	group_input_004 = crops.nodes.new("NodeGroupInput")
	group_input_004.name = "Group Input.004"

	# node Math.001
	math_001 = crops.nodes.new("ShaderNodeMath")
	math_001.name = "Math.001"
	math_001.operation = 'MULTIPLY'
	math_001.use_clamp = False
	# Value_001
	math_001.inputs[1].default_value = 1.2000000476837158
	# Value_002
	math_001.inputs[2].default_value = 0.5

	# node Math
	math = crops.nodes.new("ShaderNodeMath")
	math.name = "Math"
	math.operation = 'MULTIPLY'
	math.use_clamp = False
	# Value_001
	math.inputs[1].default_value = 0.800000011920929
	# Value_002
	math.inputs[2].default_value = 0.5

	# node Vector Math.001
	vector_math_001 = crops.nodes.new("ShaderNodeVectorMath")
	vector_math_001.name = "Vector Math.001"
	vector_math_001.operation = 'SCALE'
	# Vector_001
	vector_math_001.inputs[1].default_value = (0.0, 0.0, 0.0)
	# Vector_002
	vector_math_001.inputs[2].default_value = (0.0, 0.0, 0.0)
	# Scale
	vector_math_001.inputs[3].default_value = -1.0

	# node Random Value.003
	random_value_003 = crops.nodes.new("FunctionNodeRandomValue")
	random_value_003.name = "Random Value.003"
	random_value_003.data_type = 'FLOAT_VECTOR'
	# Min_001
	random_value_003.inputs[2].default_value = 0.0
	# Max_001
	random_value_003.inputs[3].default_value = 1.0
	# Min_002
	random_value_003.inputs[4].default_value = 0
	# Max_002
	random_value_003.inputs[5].default_value = 100
	# Probability
	random_value_003.inputs[6].default_value = 0.5
	# ID
	random_value_003.inputs[7].default_value = 0

	# node Vector.001
	vector_001 = crops.nodes.new("FunctionNodeInputVector")
	vector_001.name = "Vector.001"
	vector_001.vector = (0.009999999776482582, 0.009999999776482582, 0.0)

	# node Group Input.002
	group_input_002 = crops.nodes.new("NodeGroupInput")
	group_input_002.name = "Group Input.002"

	# node Group Output
	group_output = crops.nodes.new("NodeGroupOutput")
	group_output.name = "Group Output"
	group_output.is_active_output = True
	# crops outputs
	# output Geometry
	geometry_socket = crops.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
	geometry_socket.attribute_domain = 'POINT'



	# node Translate Instances
	translate_instances = crops.nodes.new("GeometryNodeTranslateInstances")
	translate_instances.name = "Translate Instances"
	# Selection
	translate_instances.inputs[1].default_value = True
	# Local Space
	translate_instances.inputs[3].default_value = True

	# node Realize Instances
	realize_instances = crops.nodes.new("GeometryNodeRealizeInstances")
	realize_instances.name = "Realize Instances"



	# Set parents
	vector_math.parent = frame
	random_value.parent = frame
	vector.parent = frame
	group_input_003.parent = frame
	random_value_001.parent = frame_002
	group_input_004.parent = frame_002
	math_001.parent = frame_002
	math.parent = frame_002
	vector_math_001.parent = frame_001
	random_value_003.parent = frame_001
	vector_001.parent = frame_001
	group_input_002.parent = frame_001

	# Set locations
	frame.location = (-88.02954864501953, 129.20965576171875)
	frame_002.location = (-86.45252227783203, 97.62020111083984)
	frame_001.location = (237.30496215820312, 166.27407836914062)
	instance_on_points.location = (111.75765991210938, 2.6148529052734375)
	random_value_002.location = (-387.0123596191406, 230.47996520996094)
	collection_info.location = (-391.7626647949219, 68.21037292480469)
	group_input.location = (-637.8247680664062, 140.67697143554688)
	group_input_001.location = (-92.313232421875, 325.3752746582031)
	vector_math.location = (-576.7647705078125, -266.04534912109375)
	random_value.location = (-398.885498046875, -259.322509765625)
	vector.location = (-770.3963623046875, -274.42144775390625)
	group_input_003.location = (-686.1758422851562, -414.7518615722656)
	random_value_001.location = (-383.398193359375, -668.748779296875)
	group_input_004.location = (-841.5181884765625, -702.2635498046875)
	math_001.location = (-613.4176635742188, -779.084716796875)
	math.location = (-617.5769653320312, -615.6338500976562)
	vector_math_001.location = (-174.15260314941406, -521.949462890625)
	random_value_003.location = (38.125789642333984, -515.3612060546875)
	vector_001.location = (-346.4793701171875, -534.5919189453125)
	group_input_002.location = (-197.923583984375, -682.380615234375)
	group_output.location = (1232.3245849609375, -131.56549072265625)
	translate_instances.location = (571.4591064453125, -140.4002227783203)
	realize_instances.location = (793.4547119140625, -126.73440551757812)

	# Set dimensions
	frame.width, frame.height = 571.0, 376.0
	frame_002.width, frame_002.height = 658.0, 377.0
	frame_001.width, frame_001.height = 584.0, 386.9999694824219
	instance_on_points.width, instance_on_points.height = 140.0, 100.0
	random_value_002.width, random_value_002.height = 140.0, 100.0
	collection_info.width, collection_info.height = 140.0, 100.0
	group_input.width, group_input.height = 140.0, 100.0
	group_input_001.width, group_input_001.height = 140.0, 100.0
	vector_math.width, vector_math.height = 140.0, 100.0
	random_value.width, random_value.height = 140.0, 100.0
	vector.width, vector.height = 140.0, 100.0
	group_input_003.width, group_input_003.height = 140.0, 100.0
	random_value_001.width, random_value_001.height = 140.0, 100.0
	group_input_004.width, group_input_004.height = 140.0, 100.0
	math_001.width, math_001.height = 140.0, 100.0
	math.width, math.height = 140.0, 100.0
	vector_math_001.width, vector_math_001.height = 140.0, 100.0
	random_value_003.width, random_value_003.height = 140.0, 100.0
	vector_001.width, vector_001.height = 140.0, 100.0
	group_input_002.width, group_input_002.height = 140.0, 100.0
	group_output.width, group_output.height = 140.0, 100.0
	translate_instances.width, translate_instances.height = 140.0, 100.0
	realize_instances.width, realize_instances.height = 140.0, 100.0

	# initialize crops links
	# collection_info.Instances -> instance_on_points.Instance
	crops.links.new(collection_info.outputs[0], instance_on_points.inputs[2])
	# random_value.Value -> instance_on_points.Rotation
	crops.links.new(random_value.outputs[0], instance_on_points.inputs[5])
	# vector.Vector -> vector_math.Vector
	crops.links.new(vector.outputs[0], vector_math.inputs[0])
	# vector_math.Vector -> random_value.Min
	crops.links.new(vector_math.outputs[0], random_value.inputs[0])
	# vector.Vector -> random_value.Max
	crops.links.new(vector.outputs[0], random_value.inputs[1])
	# random_value_001.Value -> instance_on_points.Scale
	crops.links.new(random_value_001.outputs[1], instance_on_points.inputs[6])
	# instance_on_points.Instances -> translate_instances.Instances
	crops.links.new(instance_on_points.outputs[0], translate_instances.inputs[0])
	# vector_001.Vector -> vector_math_001.Vector
	crops.links.new(vector_001.outputs[0], vector_math_001.inputs[0])
	# vector_math_001.Vector -> random_value_003.Min
	crops.links.new(vector_math_001.outputs[0], random_value_003.inputs[0])
	# vector_001.Vector -> random_value_003.Max
	crops.links.new(vector_001.outputs[0], random_value_003.inputs[1])
	# random_value_003.Value -> translate_instances.Translation
	crops.links.new(random_value_003.outputs[0], translate_instances.inputs[2])
	# random_value_002.Value -> instance_on_points.Selection
	crops.links.new(random_value_002.outputs[3], instance_on_points.inputs[1])
	# group_input.density -> random_value_002.Probability
	crops.links.new(group_input.outputs[1], random_value_002.inputs[6])
	# group_input.Collection -> collection_info.Collection
	crops.links.new(group_input.outputs[2], collection_info.inputs[0])
	# group_input_001.Geometry -> instance_on_points.Points
	crops.links.new(group_input_001.outputs[0], instance_on_points.inputs[0])
	# group_input.Seed -> random_value_002.Seed
	crops.links.new(group_input.outputs[3], random_value_002.inputs[8])
	# group_input_002.Seed -> random_value_003.Seed
	crops.links.new(group_input_002.outputs[3], random_value_003.inputs[8])
	# group_input_003.Seed -> random_value.Seed
	crops.links.new(group_input_003.outputs[3], random_value.inputs[8])
	# math.Value -> random_value_001.Min
	crops.links.new(math.outputs[0], random_value_001.inputs[2])
	# group_input_004.scale -> math.Value
	crops.links.new(group_input_004.outputs[4], math.inputs[0])
	# group_input_004.scale -> math_001.Value
	crops.links.new(group_input_004.outputs[4], math_001.inputs[0])
	# math_001.Value -> random_value_001.Max
	crops.links.new(math_001.outputs[0], random_value_001.inputs[3])
	# realize_instances.Geometry -> group_output.Geometry
	crops.links.new(realize_instances.outputs[0], group_output.inputs[0])
	# translate_instances.Instances -> realize_instances.Geometry
	crops.links.new(translate_instances.outputs[0], realize_instances.inputs[0])
	return crops
