## Example of a configuration file

```yaml
output_enabled: [blender, gazebo]
output:
  blender:
    type: blender_file
    filename: mixed_field.blend
  gazebo:
    type: gazebo_model
    name: mixed_field

field:
  headland_width: 8.
  swath_width: 1.57
  y_function: '.2 * sin(x * tau / 15.)'
  plants_count: 100
  swaths_count: 2
  plant_distance: .15

  swaths:
    swath1:  
      plant_type: bean
      plant_height: .12
      row_distance: .4
      rows_count: 3
    swath2:  
      plant_type: maize
      plant_height: .40
      row_distance: .785
      rows_count: 2

  noise:
    position: .008
    tilt: .05
    missing: .15
    scale: .10

  weeds:
    portulaca:
      plant_type: portulaca
    polygonum:
      plant_type: polygonum
    taraxacum:
      plant_type: taraxacum

  stones: {}
```

Here is the image corresponding to this configuration:
![configuration example](/doc/imgs/config_example.png)


## Description of the configuration format

### Root elements of the configuration file

* `field`: a block that contains the parameters of the generated field
* `output`: a block where each element correspond to a named output configuration
* `output_enabled` (optional): a list of output configuration name that are used when the program 
  is executed.
  If it is not specified, all defined output are applied.

### The `field` block

```yaml
field:
  headland_width: 7.0
  scattering_extra_width: 1.5
  swaths:
    my_swath1:
      ...
    my_swath2:
      ...
  noise: {}
  weeds:
    weed1:
      ...
    weed2:
      ...
  stones: {}
```

* `headland_width` (default: 4.0, in meters): an extra band of ground around the field.
* `scattering_extra_width` (default: 1.0, in meters): an extra band around the field used to
  generate scattering.
* `swaths`: a block that contains the configuration of each swath to generate.
  The key correspond to the name of the swath and the value is a swath block (described below).
* `noise` (optional): a block that contains the noise configuration.
* `weeds` (optional): a block that contains the configuration of each weed scattering.
* `stones` (optional): a block that contains the stones scattering configuration.

It is also possible to specify the parameters of the swath block directly in the `field` block.
In this case, these parameters are used as default values for the swaths.

#### The swath block

```yaml
my_swath1:
  plant_type: bean
  plant_height: .12
  row_distance: .52
  rows_count: 3
  swath_width: 1.57
  plants_count: 100
  swaths_count: 10
  plant_distance: .15
  shift_next_swath: false
  offset: [0., .3, 0.]
  y_function: '1.4 * sin(x * tau / 15.)'
```

It corresponds to the element of the `swaths` block of the `field`.
The key corresponds to the name of the swath.

* `plant_type`: allows to select the model group.
  The current types available are `maize` and `bean`.
* `plant_height` (in meters): the desired height for the plants.
  The models are grouped by height and are rescaled to correspond to the desired height.
* `plant_distance` (in meters): the distance between each crop in a row.
* `swath_width` (in meters): the with of the swath.
  The next swath will be generated with an offset corresponding to the `swath_width` multiplied by
  `swath_count` but only if `shift_next_swath` is disabled.
* `row_distance` (in meters): distance between two consecutive rows in the swath.
* `plants_count`: number of plants in a row.
* `rows_count` (default: 1): number of rows in a swath.
* `swaths_count` (default: 1): number of swath (the same configuration is repeated).
* `shift_next_swath` (default: true): a boolean to enable/disable the shift of the next swath.
  If disabled, the next swath configuration will cover the previous one.
* `offset` (default: [0, 0, 0], in meters): a (x,y,z) offset applied to all crops of the swath
* `y_function` (default: '0.0'): a string representing a python expression used to apply a lateral
  offset depending of the `x` coordinate.
  It is equivalent to write a function _y = f(x)_ where _y_ is the lateral offset and _x_ the
  position in the row.
  You can use the `x` variable, any functions of the python `math` module and some built-in
  functions like `abs`, `min` or `max`.

#### The `noise` block

```yaml
noise:
  position: .008
  tilt: .05
  scale: .10
  missing: .15
```

* `position` (in meters): standard deviation of a centered normal distribution.
  It is applied on the _x_ and _y_ axis of the position.
* `tilt` (in radians): standard deviation of a centered normal distribution.
  It is applied on the _roll_ and _pitch_ angle of the orientation.
* `scale` (coefficient): standard deviation of a log-normal distribution (with mu = 0)
* `missing` (between 0 and 1): probability that a crop is missing.

#### The weeds block

```yaml
weeds:
  test_weed1:
    plant_type: portulaca
    density: 3.5
  test_weed2:
    plant_type: polygonum
    density: 4.9
```

The `weeds` block of the `field` contains several key/value that correspond to a name and a
scattering configuration block.

* `plant_type`: a string that corresponds to the name of the weed model
* `density`: a float that control the quantity of weeds that is generated

#### The `stones` block

```yaml
stones:
  density: 3.8
```

* `density`: a float that control the quantity of stones that is generated


### The `output` block

```yaml
output_enabled: [out1]
output:
  out1:
    type: blender_file
    ...
  out2:
    type: gazebo_model
    ...
```

The `output` block contains several key/value that correspond to a name that can be referenced by
`output_enabled` and a configuration block:

* `type`: the output type. Available: `blender_file` or `gazebo_model`

The other parameters of the output block depends of the `type`.

#### Output type `blender_file`

```yaml
out1:
  type: blender_file
  filename: small_field.blend
```

* `filename`: file name (and optionally a relative path) of the generated blender file

#### Output type `gazebo_model`

```yaml
out2:
  type: gazebo_model
  name: maize_field
  author: John Smith
  use_absolute_path: false
```

* `name`: name (and optionally a relative path) of the gazebo model directory to create
* `author`: a string to add in the author field of the model config file
* `use_absolute_path` (default: false): a boolean to enable/disable use of absolute path for
  resources used in the SDF file.
