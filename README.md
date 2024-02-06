# CropCraft

CropCraft is python script that allows to generate 3D models of crop fields specialized for
real-time simulation of robotics application.

![Example of field](doc/field_transparent.png)


## Installation

This program uses blender as a backend.
You can dowload it on the [official website](https://www.blender.org/download/).
You also have to check that it is launchable from the command line.
It means that the `PATH` environment variable contains the directory of blender executable.

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