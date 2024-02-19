#!/usr/bin/env python3
import click
import os
import subprocess


@click.command(
    help='Generate a 3D model of an agriculutral field described using a YAML config file.')
@click.argument('config_file', type=click.Path(exists=True, readable=True))
@click.option('-d', '--output-dir', default='.', type=click.Path(writable=True),
              help='Set the destination path used by the configuration outputs.')
@click.option('-f', '--foreground', is_flag=True, help='Open blender in foreground.')
def main(config_file, output_dir, foreground):
    project_path = os.path.dirname(os.path.realpath(__file__))
    entrypoint_path = os.path.join(project_path, 'core', 'blender_entrypoint.py')
    config_path = os.path.realpath(config_file)
    output_path = os.path.realpath(output_dir)

    os.chdir(project_path)

    blender_cmd = ['blender']
    if not foreground:
        blender_cmd.append('--background')
    blender_cmd += ['--python', entrypoint_path, '--', config_path, output_path]

    subprocess.run(blender_cmd)


if __name__ == '__main__':
    main()
