import sys
import importlib
import os

if not importlib.util.find_spec('yaml'):
    import pip
    pip.main(['install', 'pyyaml', '--user'])

importlib.invalidate_caches()
yaml = importlib.import_module('yaml')

this_module_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, this_module_dir)

import core


def load_config(filename: str):
    with open(filename, 'r') as file:
        cfg = yaml.safe_load(file.read())
    return cfg


def main(argv: list):
    args = argv[argv.index('--') + 1:]
    config_file = args[0]
    output_dir = args[1] if len(args) >= 2 else '.'

    cfg = load_config(config_file)

    core.base.create_blender_context()
    
    beds = core.beds.Beds(cfg['field'])
    beds.load_plants()
    beds.create_beds()

    look_at = beds.center_pos.copy()
    look_at.x = 6.
    core.base.create_camera(look_at)


if __name__ == '__main__':
    main(sys.argv)
