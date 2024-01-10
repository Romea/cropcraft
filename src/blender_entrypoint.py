import sys
import importlib

if not importlib.util.find_spec('yaml'):
    import pip
    pip.main(['install', 'pyyaml', '--user'])

importlib.invalidate_caches()
yaml = importlib.import_module('yaml')


def load_config(filename: str):
    cfg = yaml.safe_load(filename)
    return cfg


def main(argv: list):
    args = argv[argv.index('--') + 1:]
    config_file = args[0]
    output_dir = args[1] if len(args) >= 2 else '.'

    cfg = load_config(config_file)
    print(cfg)


if __name__ == '__main__':
    main(sys.argv)
