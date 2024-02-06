# CropCraft

CropCraft is a python script that allows to generate 3D models of crop fields specialized for
real-time simulation of robotics application.

![Example of field](doc/imgs/field_demo.png)

* Designed for real-time simulation
* Suitable for use with LiDARs and cameras
* Highly configurable (YAML file)
* Provide ground truth data (identify plant types in LiDAR data)


## Requirements

This program uses blender as a backend.
It is an 3D modeling software that you can dowload from the
[official website](https://www.blender.org/download/).
You also have to check that it is launchable from the command line.
It means that blender must be accessible using the `PATH` environment variable.

You also need to install some python requirements:
```
pip install -r requirements.txt
```

## Running

To generate a crop field, you first need to create a configuration file (YAML formats).
Some examples are available in the [`examples`](/examples) directory.
Then you can execute the `cropcraft.py` script and specify the path of the choosen configuration
file.
```
python cropcraft.py examples/test1.yaml
```
This command will generate a blender file named `test1.blend` a gazebo model named `test1`

Some options are available and described using
```
python cropcraft.py --help
```
