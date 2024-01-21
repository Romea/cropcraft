import bpy

# initialize gaussian_random node group
def gaussian_random_node_group():
	gaussian_random = bpy.data.node_groups.new(type='GeometryNodeTree', name="gaussian random")

	# initialize gaussian_random nodes
	# node Frame.005
	frame_005 = gaussian_random.nodes.new("NodeFrame")
	frame_005.label = "Standard Normal Distribution"
	frame_005.name = "Frame.005"
	frame_005.use_custom_color = True
	frame_005.color = (0.2529434263706207, 0.09007680416107178, 0.010082812048494816)
	frame_005.label_size = 20
	frame_005.shrink = True

	# node Frame
	frame = gaussian_random.nodes.new("NodeFrame")
	frame.label = "2 * pi * U_2"
	frame.name = "Frame"
	frame.label_size = 20
	frame.shrink = True

	# node Frame.003
	frame_003 = gaussian_random.nodes.new("NodeFrame")
	frame_003.label = "X_1"
	frame_003.name = "Frame.003"
	frame_003.label_size = 20
	frame_003.shrink = True

	# node Frame.001
	frame_001 = gaussian_random.nodes.new("NodeFrame")
	frame_001.label = "sqrt(-2 * ln(U_1))"
	frame_001.name = "Frame.001"
	frame_001.label_size = 20
	frame_001.shrink = True

	# node Math.002
	math_002 = gaussian_random.nodes.new("ShaderNodeMath")
	math_002.name = "Math.002"
	math_002.operation = 'MULTIPLY'
	math_002.use_clamp = False
	# Value_001
	math_002.inputs[1].default_value = 6.2831854820251465
	# Value_002
	math_002.inputs[2].default_value = 0.5

	# node Random Value.001
	random_value_001 = gaussian_random.nodes.new("FunctionNodeRandomValue")
	random_value_001.label = "U_2"
	random_value_001.name = "Random Value.001"
	random_value_001.data_type = 'FLOAT'
	# Min
	random_value_001.inputs[0].default_value = (0.0, 0.0, 0.0)
	# Max
	random_value_001.inputs[1].default_value = (1.0, 1.0, 1.0)
	# Min_001
	random_value_001.inputs[2].default_value = 0.0
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

	# node Math.010
	math_010 = gaussian_random.nodes.new("ShaderNodeMath")
	math_010.name = "Math.010"
	math_010.operation = 'ADD'
	math_010.use_clamp = False
	# Value_001
	math_010.inputs[1].default_value = 1.0
	# Value_002
	math_010.inputs[2].default_value = 0.5

	# node Reroute
	reroute = gaussian_random.nodes.new("NodeReroute")
	reroute.name = "Reroute"
	# node Reroute.002
	reroute_002 = gaussian_random.nodes.new("NodeReroute")
	reroute_002.name = "Reroute.002"
	# node Reroute.001
	reroute_001 = gaussian_random.nodes.new("NodeReroute")
	reroute_001.name = "Reroute.001"
	# node Math.005
	math_005 = gaussian_random.nodes.new("ShaderNodeMath")
	math_005.name = "Math.005"
	math_005.operation = 'MULTIPLY'
	math_005.use_clamp = False
	# Value_002
	math_005.inputs[2].default_value = 0.5

	# node Math.004
	math_004 = gaussian_random.nodes.new("ShaderNodeMath")
	math_004.name = "Math.004"
	math_004.operation = 'COSINE'
	math_004.use_clamp = False
	# Value_001
	math_004.inputs[1].default_value = 0.5
	# Value_002
	math_004.inputs[2].default_value = 0.5

	# node Math.008
	math_008 = gaussian_random.nodes.new("ShaderNodeMath")
	math_008.name = "Math.008"
	math_008.operation = 'MULTIPLY'
	math_008.use_clamp = False
	# Value_002
	math_008.inputs[2].default_value = 0.5

	# node Math.007
	math_007 = gaussian_random.nodes.new("ShaderNodeMath")
	math_007.name = "Math.007"
	math_007.operation = 'ADD'
	math_007.use_clamp = False
	# Value_002
	math_007.inputs[2].default_value = 0.5

	# node Math
	math = gaussian_random.nodes.new("ShaderNodeMath")
	math.name = "Math"
	math.operation = 'LOGARITHM'
	math.use_clamp = False
	# Value_001
	math.inputs[1].default_value = 2.7182817459106445
	# Value_002
	math.inputs[2].default_value = 0.5

	# node Random Value.002
	random_value_002 = gaussian_random.nodes.new("FunctionNodeRandomValue")
	random_value_002.label = "U_1"
	random_value_002.name = "Random Value.002"
	random_value_002.data_type = 'FLOAT'
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
	# Probability
	random_value_002.inputs[6].default_value = 0.5
	# ID
	random_value_002.inputs[7].default_value = 0

	# node Math.001
	math_001 = gaussian_random.nodes.new("ShaderNodeMath")
	math_001.name = "Math.001"
	math_001.operation = 'MULTIPLY'
	math_001.use_clamp = False
	# Value_001
	math_001.inputs[1].default_value = -2.0
	# Value_002
	math_001.inputs[2].default_value = 0.5

	# node Math.003
	math_003 = gaussian_random.nodes.new("ShaderNodeMath")
	math_003.name = "Math.003"
	math_003.operation = 'SQRT'
	math_003.use_clamp = False
	# Value_001
	math_003.inputs[1].default_value = 0.5
	# Value_002
	math_003.inputs[2].default_value = 0.5

	# node Group Output
	group_output = gaussian_random.nodes.new("NodeGroupOutput")
	group_output.name = "Group Output"
	group_output.is_active_output = True
	# gaussian_random outputs
	# output Value
	value_socket = gaussian_random.interface.new_socket(name = "Value", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
	value_socket.subtype = 'NONE'
	value_socket.default_value = 0.0
	value_socket.min_value = -3.4028234663852886e+38
	value_socket.max_value = 3.4028234663852886e+38
	value_socket.attribute_domain = 'POINT'



	# node Group Input
	group_input = gaussian_random.nodes.new("NodeGroupInput")
	group_input.name = "Group Input"
	# gaussian_random inputs
	# input Mean
	mean_socket = gaussian_random.interface.new_socket(name = "Mean", in_out='INPUT', socket_type = 'NodeSocketFloat')
	mean_socket.subtype = 'NONE'
	mean_socket.default_value = 0.0
	mean_socket.min_value = -10000.0
	mean_socket.max_value = 10000.0
	mean_socket.attribute_domain = 'POINT'

	# input Std. Dev.
	std__dev__socket = gaussian_random.interface.new_socket(name = "Std. Dev.", in_out='INPUT', socket_type = 'NodeSocketFloat')
	std__dev__socket.subtype = 'NONE'
	std__dev__socket.default_value = 1.0
	std__dev__socket.min_value = -10000.0
	std__dev__socket.max_value = 10000.0
	std__dev__socket.attribute_domain = 'POINT'

	# input Seed
	seed_socket = gaussian_random.interface.new_socket(name = "Seed", in_out='INPUT', socket_type = 'NodeSocketInt')
	seed_socket.subtype = 'NONE'
	seed_socket.default_value = 70
	seed_socket.min_value = -10000
	seed_socket.max_value = 10000
	seed_socket.attribute_domain = 'POINT'





	# Set parents
	frame.parent = frame_005
	frame_003.parent = frame_005
	frame_001.parent = frame_005
	math_002.parent = frame
	random_value_001.parent = frame
	math_005.parent = frame_003
	math_004.parent = frame_003
	math.parent = frame_001
	random_value_002.parent = frame_001
	math_001.parent = frame_001
	math_003.parent = frame_001

	# Set locations
	frame_005.location = (-1112.0865478515625, -128.85238647460938)
	frame.location = (259.01312255859375, -302.9204406738281)
	frame_003.location = (873.2244873046875, -103.39718627929688)
	frame_001.location = (91.21820068359375, -54.144927978515625)
	math_002.location = (138.8717041015625, -30.349945068359375)
	random_value_001.location = (-49.1328125, -22.685699462890625)
	math_010.location = (-1260.0977783203125, -387.19256591796875)
	reroute.location = (-1314.0389404296875, -347.5232849121094)
	reroute_002.location = (-40.4051513671875, -54.46783447265625)
	reroute_001.location = (-40.4051513671875, -90.31451416015625)
	math_005.location = (197.912353515625, -20.78594970703125)
	math_004.location = (19.02197265625, -150.98068237304688)
	math_008.location = (279.7392578125, -196.01165771484375)
	math_007.location = (465.760498046875, -48.5018310546875)
	math.location = (163.855224609375, -4.512359619140625)
	random_value_002.location = (-18.83349609375, -5.126068115234375)
	math_001.location = (343.5445556640625, -6.446319580078125)
	math_003.location = (563.8683471679688, -15.1051025390625)
	group_output.location = (711.092529296875, -88.436279296875)
	group_input.location = (-1518.024658203125, -22.1375732421875)

	# Set dimensions
	frame_005.width, frame_005.height = 1259.0, 559.0
	frame.width, frame.height = 388.0, 232.99996948242188
	frame_003.width, frame_003.height = 379.0, 322.0
	frame_001.width, frame_001.height = 783.0, 233.0
	math_002.width, math_002.height = 140.0, 100.0
	random_value_001.width, random_value_001.height = 140.0, 100.0
	math_010.width, math_010.height = 140.0, 100.0
	reroute.width, reroute.height = 16.0, 100.0
	reroute_002.width, reroute_002.height = 16.0, 100.0
	reroute_001.width, reroute_001.height = 16.0, 100.0
	math_005.width, math_005.height = 140.0, 100.0
	math_004.width, math_004.height = 140.0, 100.0
	math_008.width, math_008.height = 140.0, 100.0
	math_007.width, math_007.height = 140.0, 100.0
	math.width, math.height = 140.0, 100.0
	random_value_002.width, random_value_002.height = 140.0, 100.0
	math_001.width, math_001.height = 140.0, 100.0
	math_003.width, math_003.height = 140.0, 100.0
	group_output.width, group_output.height = 140.0, 100.0
	group_input.width, group_input.height = 140.0, 100.0

	# initialize gaussian_random links
	# random_value_002.Value -> math.Value
	gaussian_random.links.new(random_value_002.outputs[1], math.inputs[0])
	# math.Value -> math_001.Value
	gaussian_random.links.new(math.outputs[0], math_001.inputs[0])
	# random_value_001.Value -> math_002.Value
	gaussian_random.links.new(random_value_001.outputs[1], math_002.inputs[0])
	# math_002.Value -> math_004.Value
	gaussian_random.links.new(math_002.outputs[0], math_004.inputs[0])
	# math_003.Value -> math_005.Value
	gaussian_random.links.new(math_003.outputs[0], math_005.inputs[0])
	# reroute.Output -> random_value_002.Seed
	gaussian_random.links.new(reroute.outputs[0], random_value_002.inputs[8])
	# group_input.Seed -> reroute.Input
	gaussian_random.links.new(group_input.outputs[2], reroute.inputs[0])
	# reroute.Output -> math_010.Value
	gaussian_random.links.new(reroute.outputs[0], math_010.inputs[0])
	# math_010.Value -> random_value_001.Seed
	gaussian_random.links.new(math_010.outputs[0], random_value_001.inputs[8])
	# group_input.Std. Dev. -> reroute_001.Input
	gaussian_random.links.new(group_input.outputs[1], reroute_001.inputs[0])
	# group_input.Mean -> reroute_002.Input
	gaussian_random.links.new(group_input.outputs[0], reroute_002.inputs[0])
	# reroute_001.Output -> math_008.Value
	gaussian_random.links.new(reroute_001.outputs[0], math_008.inputs[0])
	# reroute_002.Output -> math_007.Value
	gaussian_random.links.new(reroute_002.outputs[0], math_007.inputs[0])
	# math_008.Value -> math_007.Value
	gaussian_random.links.new(math_008.outputs[0], math_007.inputs[1])
	# math_007.Value -> group_output.Value
	gaussian_random.links.new(math_007.outputs[0], group_output.inputs[0])
	# math_005.Value -> math_008.Value
	gaussian_random.links.new(math_005.outputs[0], math_008.inputs[1])
	# math_004.Value -> math_005.Value
	gaussian_random.links.new(math_004.outputs[0], math_005.inputs[1])
	# math_001.Value -> math_003.Value
	gaussian_random.links.new(math_001.outputs[0], math_003.inputs[0])
	return gaussian_random
