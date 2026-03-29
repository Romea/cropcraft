# How to add your own assets

All the default models and textures are stored in the [assets](assets) directory.
The folder is organized as follows:

* `plants` contains sub-folders corresponding to different type of plants you can use for the
  `plant_type` parameter of the beds and the weeds in the configuration file
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

To create a new plant type that can be used in a bed or as weeds, export the 3D model as either:

- Wavefront **OBJ** (`.obj`)
- **USD** (`.usd`, `.usda`, `.usdc`, or `.usdz`)

Place the file in a sub-directory of `plants`. The name of this sub-directory is the ID you’ll use for the `plant_type` parameter in your config.

- **OBJ:** put the `.mtl` and any textures in the *same* directory as the `.obj`.
- **USD:** you can keep materials and textures alongside the USD file, and you may also organize assets in neat subfolders. For example:
  - `plants/leek/leaf1/leaf.usd`
  - `plants/leek/leaf1/textures/...`
  
  As long as the USD can be imported properly in Blender with all of its references (materials, textures, payloads/references), it will work here too. If you prefer everything bundled, a `.usdz` package is also supported.

If you have multiple versions of the same plant, create a separate model file for each variant (you can mix OBJ and USD in the same plant type).

You must also create a `description.yaml` or `description.json` file with metadata for your models. Example `description.yaml`:

```yaml
models:
  - filename: sorghum_small_01.usdc
    height: 0.12
    width: 0.08
    leaf_area: 0.352
  - filename: sorghum_small_02.usda
    height: 0.16
    width: 0.09
    leaf_area: 0.390
  - filename: leaf1/leaf.usd
    height: 0.20
    width: 0.12
    leaf_area: 0.420
  - filename: sorghum_big_01.obj
    height: 0.47
    width: 0.31
    leaf_area: 0.648
```


For each model, you have to specify the following elements:

* `filename`: the name of the 3D file
* `height` (in meters): the height of the plant
* `width` (optional, in meters): the width of the plant
* `leaf_area` (optional, in square meters): the leaf area of the plant

If the model is used in the `weeds` field of the configuration file, only the smallest height group
is used.

Multiple textures will not be read from the `.mtl` file properly. You should build your models either from a single texture `.jpg`, or use a script similar to that used in assets/plants/apple which corrects for this later.