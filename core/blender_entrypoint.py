import sys
import os

this_module_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, this_module_dir)

import core


def main(argv: list):
    args = argv[argv.index('--') + 1:]
    config_file = args[0]
    output_dir = args[1] if len(args) >= 2 else '.'

    try:
        cfg = core.parser.load_yaml_config(config_file)
    except core.parser.ParserError as e:
        print(f"Error: Failed to load config file '{config_file}': {e}", file=sys.stderr)
        exit(1)

    core.base.create_blender_context()
    
    beds = core.beds.Beds(cfg.field)
    beds.load_plants()
    beds.create_beds()

    weeds = core.ground.Ground(cfg.field)
    # weeds.load_weeds()

    look_at = beds.center_pos.copy()
    look_at.x = 6.
    core.base.create_camera(look_at)

    for output in cfg.outputs:
        output.export(output_dir)


if __name__ == '__main__':
    main(sys.argv)
