# How to add your own assets

All the default models and textures are stored in the [assets](assets) directory.
The folder is organized as follows:

* `plants` contains sub-folders corresponding to different type of plants you can use for the
  `plant_type` parameter of the swaths in the configuration file
* `stones` contains models used by the `stones` block of the configuration file
* `textures` contains the texture file of the ground
* `weeds` contains sub-folders corresponding to different type of weeds you can use for the
  `plant_type` parameter of the weeds block in the configuration file

If you want to add your own models, you can create the same folders in

* `~/.local/share/cropcraft` if you use Linux
* `C:\Users\<username>\AppData\Local\cropcraft` if you use Windows
* `/Users/<username>/Library/Application Support/cropcraft` if you use Mac OS X

For example, if you use Linux, you can add a leek model by creating the directory 
`~/.local/share/cropcraft/plants/leek/`.


## Add a plant type

To create a new plant type that can be used in a swath, you need to export the 3D model as a
Wavefront (`.obj`) model in a sub-directory of `plants`.
The name of this sub-directory corresponds to the ID to use for the `plant_type` parameter of a
swath block in a configuration file.
If your model have a material and a texture file, it can be placed in the same directory as the
`.obj` file.
If you have different versions of the same plant, you need to create a separate `.obj` file for
each model.

You must also create a `description.yaml` or `description.json` file that contains metadatas about
the models.
Here is an example of a `description.yaml` file:

```yaml
model_groups:
  small:
    minimal_height: 0.
    models:
      - filename: sorghum_small_01.obj
        height: 0.12
        width: 0.08
        leaf_area: 0.352
      - filename: sorghum_small_02.obj
        height: 0.16
        width: 0.09
        leaf_area: 0.390
  big:
    minimal_height: 0.40
    models:
      - filename: sorghum_big_01.obj
        height: 0.47
        width: 0.31
        leaf_area: 0.648
      - filename: sorghum_big_02.obj
        height: 0.43
        width: 0.28
        leaf_area: 0.713
```

The models are separated into several `model_groups`.
For each one, you have to specify the `minimal_height`.
This parameter is compared to the desired height defined in the swath configuration and allows to
select the correct model group used to generate the swath.

For each model, you have to specify the following elements:

* `filename`: the name of the 3D file
* `height` (in meters): the height of the plant
* `width` (optional, in meters): the width of the plant
* `leaf_area` (optional, in square meters): the leaf area of the plant


## Add a weed type

To create a new weed type that can be used in a field, you need to export the 3D model as a
Wavefront (`.obj`) model in a sub-directory of `weeds`.
The name of this sub-directory corresponds to the ID to use for the `plant_type` parameter of a
weeds block in a configuration file.
If your model have a material and a texture file, it can be placed in the same directory as the
`.obj` file.
If you have different versions of the same plant, you need to create a separate `.obj` file for
each model.
The scattering algorithm will pick a random model among the ones present in this directory.
