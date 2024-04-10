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
      density: 3.
    polygonum:
      plant_type: polygonum
      distance_min: 0.16
    taraxacum:
      plant_type: taraxacum
      density: 10.
      noise_offset: -0.1

  stones:
    density: 60.
    noise_scale: 0.24
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
  random_seed: 344567809264
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
* `random_seed` (optional): integer used to initialize the random number generator.
  If this element is specified, the generated environment will always be the same if the program is
  executed several times with no change in its configuration.
  The program outputs its seed in order to use it in a configuration file and generate a similar
  environment.
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
  aligned: false
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
* `orientation` (choice: [random, aligned, zero], default: random): if the orientation is `random`,
  the plant is oriented using a uniform distribution between 0° and 360°.
  If it is `aligned`, the angle will be 0° or 180°.
  If it is `zero`, the angle will be only 0°.

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
    distance_min: 0.15
    noise_scale: 0.29
    noise_offset: 0.21
  test_weed2:
    plant_type: polygonum
    density: 4.9
```

The `weeds` block of the `field` contains several key/value that correspond to a name and a
scattering configuration block.

* `plant_type`: a string that corresponds to the name of the weed model
* `density`: a float that control the quantity of weeds that is generated
* `distance_min` (in meters, default: 0.12): minimal distance between generated weeds
* `scattering_mode` (default:'noise'): a string setting the mode of the scattering.
'noise' uses a random pattern controlled by the parameters `noise_scale` and `noise_offset`.
'image' uses a grayscale image to control the density
* `noise_scale` (default: 0.36): a float that control the size of the roughness of the random
  density map.
  If the value is smaller, the blob will be bigger.
* `noise_offset` (between -1.0 and 1.0, default: 0.1): a float that control the thickness of the
  empty area.
  If the value is smaller, the empty area will be bigger.
* `scattering_img`: the density image path (relative to the configuration file)

#### The `stones` block

```yaml
stones:
  density: 50.0
  distance_min: 0.04
  noise_scale: 0.36
  noise_offset: 0.23
```

* `density`: a float that control the quantity of stones that is generated
* `distance_min` (in meters, default: 0.04): minimal distance between generated stones
* `noise_scale` (default: 0.36): a float that control the size of the roughness of the random
  density map.
  If the value is smaller, the blob will be bigger.
* `noise_offset` (between -1.0 and 1.0, default: 0.23): a float that control the thickness of the
  empty area.
  If the value is smaller, the empty area will be bigger.


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
