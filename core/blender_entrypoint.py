import sys
import importlib
import os

if not importlib.util.find_spec('yaml'):
    import pip
    pip.main(['install', 'pyyaml', '--user'])

importlib.invalidate_caches()
yaml = importlib.import_module('yaml')

this_module_dir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(this_module_dir)

from beds import create_beds


def load_config(filename: str):
    with open(filename, 'r') as file:
        cfg = yaml.safe_load(file.read())
    return cfg


def main(argv: list):
    args = argv[argv.index('--') + 1:]
    config_file = args[0]
    output_dir = args[1] if len(args) >= 2 else '.'

    cfg = load_config(config_file)
    create_beds(cfg)


if __name__ == '__main__':
    main(sys.argv)
