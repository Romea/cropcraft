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

def stones_scattering_node_group():
    scattering = bpy.data.node_groups.new(type='GeometryNodeTree', name="stones_scattering")

    scattering.is_modifier = True

    # initialize scattering nodes
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

    # node Group Input.001
    group_input_001 = scattering.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    # scattering inputs
    # input Geometry
    geometry_socket = scattering.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    # input Density Factor
    density_factor_socket = scattering.interface.new_socket(name = "Density Factor", in_out='INPUT', socket_type = 'NodeSocketFloat')
    density_factor_socket.subtype = 'FACTOR'
    density_factor_socket.default_value = 1.0
    density_factor_socket.min_value = 0.0
    density_factor_socket.max_value = 1.0
    density_factor_socket.attribute_domain = 'POINT'

    # input Collection
    collection_socket = scattering.interface.new_socket(name = "Collection", in_out='INPUT', socket_type = 'NodeSocketCollection')
    collection_socket.attribute_domain = 'POINT'

    # input Seed
    seed_socket = scattering.interface.new_socket(name = "Seed", in_out='INPUT', socket_type = 'NodeSocketInt')
    seed_socket.subtype = 'NONE'
    seed_socket.default_value = 15
    seed_socket.min_value = -2147483648
    seed_socket.max_value = 2147483647
    seed_socket.attribute_domain = 'POINT'

    # input Distance Min
    distance_min_socket = scattering.interface.new_socket(name = "Distance Min", in_out='INPUT', socket_type = 'NodeSocketFloat')
    distance_min_socket.subtype = 'DISTANCE'
    distance_min_socket.default_value = 0.03999999910593033
    distance_min_socket.min_value = 0.0
    distance_min_socket.max_value = 3.4028234663852886e+38
    distance_min_socket.attribute_domain = 'POINT'

    # input Density
    density_socket = scattering.interface.new_socket(name = "Density", in_out='INPUT', socket_type = 'NodeSocketFloat')
    density_socket.subtype = 'NONE'
    density_socket.default_value = 50.0
    density_socket.min_value = 0.0
    density_socket.max_value = 1000.0
    density_socket.attribute_domain = 'POINT'

    # input Noise Scale
    noise_scale_socket = scattering.interface.new_socket(name = "Noise Scale", in_out='INPUT', socket_type = 'NodeSocketFloat')
    noise_scale_socket.subtype = 'NONE'
    noise_scale_socket.default_value = 0.36000001430511475
    noise_scale_socket.min_value = 0.0
    noise_scale_socket.max_value = 3.4028234663852886e+38
    noise_scale_socket.attribute_domain = 'POINT'

    # input Noise Offset
    noise_offset_socket = scattering.interface.new_socket(name = "Noise Offset", in_out='INPUT', socket_type = 'NodeSocketFloat')
    noise_offset_socket.subtype = 'NONE'
    noise_offset_socket.default_value = 0.23000000417232513
    noise_offset_socket.min_value = -1.0
    noise_offset_socket.max_value = 1.0
    noise_offset_socket.attribute_domain = 'POINT'



    # node Distribute Points on Faces
    distribute_points_on_faces = scattering.nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = 'POISSON'
    distribute_points_on_faces.use_legacy_normal = True
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True
    # Density
    distribute_points_on_faces.inputs[4].default_value = 10.0

    # node Group Input
    group_input = scattering.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # node Noise Texture
    if bpy.app.version >= (4, 1, 0):
        noise_texture = scattering.nodes.new("ShaderNodeTexNoise")
        noise_texture.name = "Noise Texture"
        noise_texture.noise_dimensions = '4D'
        noise_texture.noise_type = 'HETERO_TERRAIN'
        # Vector
        noise_texture.inputs[0].default_value = (0.0, 0.0, 0.0)
        # Detail
        noise_texture.inputs[3].default_value = 7.09999942779541
        # Roughness
        noise_texture.inputs[4].default_value = 0.423179030418396
        # Lacunarity
        noise_texture.inputs[5].default_value = 2.599998712539673
        # Gain
        noise_texture.inputs[7].default_value = 1.0
        # Distorsion
        noise_texture.inputs[8].default_value = 0.0
    else:
        noise_texture = scattering.nodes.new("ShaderNodeTexMusgrave")
        noise_texture.name = "Musgrave Texture"
        noise_texture.musgrave_dimensions = '4D'
        noise_texture.musgrave_type = 'HETERO_TERRAIN'
        # Vector
        noise_texture.inputs[0].default_value = (0.0, 0.0, 0.0)
        # Detail
        noise_texture.inputs[3].default_value = 7.09999942779541
        # Dimension
        noise_texture.inputs[4].default_value = 0.9000000953674316
        # Lacunarity
        noise_texture.inputs[5].default_value = 2.599998712539673
        # Gain
        noise_texture.inputs[7].default_value = 1.0

    # node Random Value.001
    random_value_001 = scattering.nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.data_type = 'FLOAT'
    # Min
    random_value_001.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Max
    random_value_001.inputs[1].default_value = (0.0, 0.0, 6.283199787139893)
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

    # node Float Curve
    float_curve = scattering.nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    # mapping settings
    float_curve.mapping.extend = 'EXTRAPOLATED'
    float_curve.mapping.tone = 'STANDARD'
    float_curve.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve.mapping.clip_min_x = 0.0
    float_curve.mapping.clip_min_y = 0.0
    float_curve.mapping.clip_max_x = 1.0
    float_curve.mapping.clip_max_y = 1.0
    float_curve.mapping.use_clip = True
    # curve 0
    float_curve_curve_0 = float_curve.mapping.curves[0]
    float_curve_curve_0_point_0 = float_curve_curve_0.points[0]
    float_curve_curve_0_point_0.location = (0.0, 0.20625007152557373)
    float_curve_curve_0_point_0.handle_type = 'AUTO'
    float_curve_curve_0_point_1 = float_curve_curve_0.points[1]
    float_curve_curve_0_point_1.location = (0.686363935470581, 0.38749992847442627)
    float_curve_curve_0_point_1.handle_type = 'AUTO'
    float_curve_curve_0_point_2 = float_curve_curve_0.points.new(0.9545454978942871, 0.5250000357627869)
    float_curve_curve_0_point_2.handle_type = 'AUTO'
    float_curve_curve_0_point_3 = float_curve_curve_0.points.new(0.9818181991577148, 0.6874999403953552)
    float_curve_curve_0_point_3.handle_type = 'AUTO'
    float_curve_curve_0_point_4 = float_curve_curve_0.points.new(1.0, 0.8687497973442078)
    float_curve_curve_0_point_4.handle_type = 'AUTO'
    # update curve after changes
    float_curve.mapping.update()
    # Factor
    float_curve.inputs[0].default_value = 1.0

    # node Realize Instances
    realize_instances = scattering.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"

    # node Group Output
    group_output = scattering.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    # scattering outputs
    # output Geometry
    geometry_socket = scattering.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'



    # node Instance on Points
    instance_on_points = scattering.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = True
    # Instance Index
    instance_on_points.inputs[4].default_value = 0

    # node Math
    math = scattering.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 2.0
    # Value_002
    math.inputs[2].default_value = 0.5

    # node Group Input.002
    group_input_002 = scattering.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"




    # Set locations
    collection_info.location = (-11.898445129394531, 59.760009765625)
    random_value.location = (-15.9769926071167, -103.20598602294922)
    group_input_001.location = (-234.2644805908203, -122.54707336425781)
    distribute_points_on_faces.location = (-205.88148498535156, 223.9701690673828)
    group_input.location = (-419.29541015625, 220.286376953125)
    noise_texture.location = (-425.44464111328125, -26.346969604492188)
    random_value_001.location = (-18.747467041015625, -406.926513671875)
    float_curve.location = (157.416015625, -174.0141143798828)
    realize_instances.location = (798.1691284179688, 43.14290237426758)
    group_output.location = (976.8123779296875, 44.46487045288086)
    instance_on_points.location = (613.274169921875, 23.789169311523438)
    math.location = (438.52020263671875, -167.2227325439453)
    group_input_002.location = (-612.51513671875, -51.7193717956543)

    # Set dimensions
    collection_info.width, collection_info.height = 140.0, 100.0
    random_value.width, random_value.height = 140.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    distribute_points_on_faces.width, distribute_points_on_faces.height = 170.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    noise_texture.width, noise_texture.height = 150.0, 100.0
    random_value_001.width, random_value_001.height = 140.0, 100.0
    float_curve.width, float_curve.height = 240.0, 100.0
    realize_instances.width, realize_instances.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0

    # initialize scattering links
    # distribute_points_on_faces.Points -> instance_on_points.Points
    scattering.links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])
    # collection_info.Instances -> instance_on_points.Instance
    scattering.links.new(collection_info.outputs[0], instance_on_points.inputs[2])
    # random_value.Value -> instance_on_points.Rotation
    scattering.links.new(random_value.outputs[0], instance_on_points.inputs[5])
    # group_input.Seed -> distribute_points_on_faces.Seed
    scattering.links.new(group_input.outputs[3], distribute_points_on_faces.inputs[6])
    # group_input.Distance Min -> distribute_points_on_faces.Distance Min
    scattering.links.new(group_input.outputs[4], distribute_points_on_faces.inputs[2])
    # realize_instances.Geometry -> group_output.Geometry
    scattering.links.new(realize_instances.outputs[0], group_output.inputs[0])
    # group_input.Geometry -> distribute_points_on_faces.Mesh
    scattering.links.new(group_input.outputs[0], distribute_points_on_faces.inputs[0])
    # noise_texture.Fac -> distribute_points_on_faces.Density Factor
    scattering.links.new(noise_texture.outputs[0], distribute_points_on_faces.inputs[5])
    # instance_on_points.Instances -> realize_instances.Geometry
    scattering.links.new(instance_on_points.outputs[0], realize_instances.inputs[0])
    # group_input_001.Collection -> collection_info.Collection
    scattering.links.new(group_input_001.outputs[2], collection_info.inputs[0])
    # group_input_001.Seed -> random_value_001.Seed
    scattering.links.new(group_input_001.outputs[3], random_value_001.inputs[8])
    # group_input_001.Seed -> random_value.Seed
    scattering.links.new(group_input_001.outputs[3], random_value.inputs[8])
    # group_input_002.Seed -> noise_texture.W
    scattering.links.new(group_input_002.outputs[3], noise_texture.inputs[1])
    # group_input.Density -> distribute_points_on_faces.Density Max
    scattering.links.new(group_input.outputs[5], distribute_points_on_faces.inputs[3])
    # group_input_002.Noise Scale -> noise_texture.Scale
    scattering.links.new(group_input_002.outputs[6], noise_texture.inputs[2])
    # group_input_002.Noise Offset -> noise_texture.Offset
    scattering.links.new(group_input_002.outputs[7], noise_texture.inputs[6])
    # math.Value -> instance_on_points.Scale
    scattering.links.new(math.outputs[0], instance_on_points.inputs[6])
    # random_value_001.Value -> float_curve.Value
    scattering.links.new(random_value_001.outputs[1], float_curve.inputs[1])
    # float_curve.Value -> math.Value
    scattering.links.new(float_curve.outputs[0], math.inputs[0])
    return scattering
