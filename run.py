#!/usr/bin/env python3
import click
import os
import subprocess


@click.command()
@click.argument('config_file', type=click.Path(exists=True, readable=True))
@click.option('-d', '--output-dir', default='.', type=click.Path(writable=True))
def main(config_file, output_dir):
    project_path = os.path.dirname(os.path.realpath(__file__))
    entrypoint_path = project_path + '/src/blender_entrypoint.py'
    config_path = os.path.realpath(config_file)
    output_path = os.path.realpath(output_dir)

    subprocess.run(['blender', '-b', '-P', entrypoint_path, '--', config_path, output_path])


if __name__ == '__main__':
    main()
