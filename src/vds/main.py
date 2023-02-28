import argparse
import importlib.util
import os
import sys
from pathlib import Path
from typing import List

from colorama import Fore, Style
from rich.console import Console  # type: ignore  # pylint: disable=import-error
from rich.table import Table  # type: ignore  # pylint: disable=import-error

from vds.config import Config, ValidDataSetPlugin  # type: ignore
from vds.colorizer import Colorizer  # type: ignore


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(description='Validate audio and text files.')
    argument_parser.add_argument(
        '-p', '--path', type=Path, action='store', required=False, default='wavs',
        help='Path to dataset',
    )
    argument_parser.add_argument(
        '-d', '--disable', type=str, action='store', required=False, default='',
        help='Disable plugins',
    )
    argument_parser.add_argument(
        '-f', '--files', type=str, action='store', required=False, default='list_train.txt,list_val.txt',
        help='Set transcription file names',
    )
    argument_parser.add_argument('--list-plugins', action='store_true', help='List plugins')

    argument_parser.add_argument(
        '-v', '--verbose', action='store_true', required=False, default=False,
        help='Print additional information',
    )
    return argument_parser


def list_plugins() -> None:
    plugin_modules = get_plugins()

    table = Table(title='Plugins')

    table.add_column('ID', justify='center', style='cyan', no_wrap=True)
    table.add_column('Name', justify='left', style='magenta', no_wrap=True)
    table.add_column('Version', justify='center', style='yellow', no_wrap=True)
    table.add_column('Description', justify='left', style='green', no_wrap=True)

    for valid_dataset_plugin in plugin_modules:
        vds_plugin = valid_dataset_plugin.init_plugin()
        table.add_row(vds_plugin.info.id, vds_plugin.info.name, vds_plugin.info.version, vds_plugin.info.description)
    console = Console()
    console.print(table)
    print()


def get_plugins() -> List[ValidDataSetPlugin]:
    Config.disabled_plugins = [f'{file.lower()}.py' for file in Config.arguments.disable.split(',')]

    Config.transcription_plugins_dir_path = str(
        Path(__file__).parent / 'plugins' / Config.transcription_plugins_dir_path,
    )
    Config.files_plugins_dir_path = str(
        Path(__file__).parent / 'plugins' / Config.files_plugins_dir_path,
    )

    Config.activate_plugins = [
        file for file in (
            os.listdir(Path(__file__).parent / 'plugins' / Config.transcription_plugins_dir_path)
            + os.listdir(Path(__file__).parent / 'plugins' / Config.files_plugins_dir_path)
        ) if file.endswith('.py') and file not in Config.disabled_plugins
    ]

    plugin_modules = []

    for plugin_file in sorted(Config.activate_plugins):
        module_name: str = str(os.path.splitext(plugin_file)[0])
        module_path: str = ''
        if 't' in plugin_file:
            module_path = str(Path(Config.transcription_plugins_dir_path) / str(plugin_file))
        elif 'f' in plugin_file:
            module_path = str(Path(Config.files_plugins_dir_path) / str(plugin_file))

        spec = importlib.util.spec_from_file_location(str(module_name), module_path)
        if spec is None:
            continue
        plugin_module = importlib.util.module_from_spec(spec)
        if spec.loader is not None:
            spec.loader.exec_module(plugin_module)
        plugin_modules.append(plugin_module)
    return plugin_modules


def main() -> None:
    Config.arguments = parser().parse_args()

    if Config.arguments.list_plugins:
        list_plugins()
        sys.exit(0)

    colorizer = Colorizer()

    _status_ok = f'{Fore.GREEN}{Style.BRIGHT} OK {Style.RESET_ALL}'
    _status_fail = f'{Fore.RED}{Style.BRIGHT}FAIL{Style.RESET_ALL}'

    plugin_modules = get_plugins()

    for valid_dataset_plugin in plugin_modules:
        vds_plugin = valid_dataset_plugin.init_plugin()

        colored_id = f'{Fore.LIGHTRED_EX}{Style.BRIGHT}{vds_plugin.info.id}{Style.RESET_ALL}'

        vds_plugin.run(
            Config.arguments.path, tuple(Path(path) for path in str(Config.arguments.files).split(',')), 'wavs',
        )

        if len(vds_plugin.errors) == 0 and Config.arguments.verbose:
            print(f'{colored_id}: [{_status_ok}] {vds_plugin.success_message}\n')

        if len(vds_plugin.errors) > 0:
            print(f'{colored_id}: [{_status_fail}] {vds_plugin.error_message}\n')
            for error in vds_plugin.errors:
                print(colorizer.colorize(error))
            print()


if __name__ == '__main__':
    main()
