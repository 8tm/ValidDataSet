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

    # ARGS menu:
    argument_parser.add_argument(
        '--args.files', type=str, default='list_train.txt,list_val.txt',
        dest='args_files', help='Set transcription file names',
    )
    argument_parser.add_argument(
        '--args.dir-name', type=str, action='store', required=False, default='wavs',
        dest='args_dir_name', help='Name of folder with wav files',
    )
    argument_parser.add_argument(
        '--args.path', type=str, action='store', required=False, default='',
        dest='args_path', help='Path to dataset',
    )
    argument_parser.add_argument(
        '--args.sample-rate', type=int, action='store', required=False, default=22050,
        dest='args_sample_rate', help='Set sample rate',
    )
    argument_parser.add_argument(
        '--args.number-of-channels', type=int, action='store', required=False, default=1,
        dest='args_number_of_channels', help='Set number of channels',
    )
    argument_parser.add_argument(
        '--args.min-duration', type=int, action='store', required=False, default=2000,
        dest='args_min_duration', help='Set minimum duration in miliseconds (1 second = 1000 milisecond)',
    )
    argument_parser.add_argument(
        '--args.max-duration', type=int, action='store', required=False, default=10000,
        dest='args_max_duration', help='Set maximum duration in miliseconds (1 second = 1000 milisecond)',
    )
    argument_parser.add_argument(
        '--args.number-of-pipes', type=int, action='store', required=False, default=1,
        dest='args_number_of_pipes', help='Set number of pipes in transcripton files',
    )

    # PLUGINS menu:
    argument_parser.add_argument(
        '--plugins.disable', type=str, action='store', required=False, default='',
        dest='plugins_disable', help='Disable plugins',
    )

    argument_parser.add_argument(
        '--plugins.list', action='store_true',
        dest='plugins_list', help='List plugins',
    )

    # MAIN menu:
    argument_parser.add_argument(
        '-o', '--output', type=Path, action='store', required=False, default=None,
        help='Save output to file',
    )

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
    Config.disabled_plugins = [f'{file.lower()}.py' for file in Config.arguments.plugins_disable.split(',')]

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


def add_text_to_file(path: Path, text: str) -> None:
    with open(path, 'a', encoding='UTF-8') as file:
        file.write(text)


def present_plugin_output(vds_plugin: ValidDataSetPlugin, colorizer: Colorizer) -> None:
    _status_ok = f'{Fore.GREEN}{Style.BRIGHT} OK {Style.RESET_ALL}'
    _status_fail = f'{Fore.RED}{Style.BRIGHT}FAIL{Style.RESET_ALL}'
    colored_id = f'{Fore.LIGHTRED_EX}{Style.BRIGHT}{vds_plugin.info.id}{Style.RESET_ALL}'

    if len(vds_plugin.errors) == 0 and Config.arguments.verbose:
        line = f'{colored_id}: [{_status_ok}] {vds_plugin.success_message}\n'

        if Config.arguments.output:
            add_text_to_file(Config.arguments.output, line)

        print(line)

    if len(vds_plugin.errors) > 0:
        bright_error_message = f'{Fore.WHITE}{Style.NORMAL}{vds_plugin.error_message}{Style.RESET_ALL}'
        line = f'{colored_id}: [{_status_fail}] {bright_error_message.format(nof=str(len(vds_plugin.errors)))}\n'

        if Config.arguments.output:
            add_text_to_file(Config.arguments.output, line)

        print(line)

        for error in vds_plugin.errors:

            if Config.arguments.output:
                add_text_to_file(Config.arguments.output, colorizer.colorize(error))

            print(colorizer.colorize(error))
        print()


def main() -> None:
    Config.arguments = parser().parse_args()

    if Config.arguments.plugins_list:
        list_plugins()
        sys.exit(0)

    if Config.arguments.output and Path(Config.arguments.output).exists():
        Path(Config.arguments.output).unlink()

    colorizer = Colorizer()

    plugin_modules = get_plugins()

    for valid_dataset_plugin in plugin_modules:

        vds_plugin = valid_dataset_plugin.init_plugin()
        vds_plugin.args = {
            'path': str(Config.arguments.args_path),
            'files': list(path for path in str(Config.arguments.args_files).split(',')),
            'dir_name': str(Config.arguments.args_dir_name),
            'expected_properties': {
                'sample_rate': Config.arguments.args_sample_rate,
                'number_of_channels': Config.arguments.args_number_of_channels,
                'min_duration': Config.arguments.args_min_duration,
                'max_duration': Config.arguments.args_max_duration,
                'number_of_pipes': Config.arguments.args_number_of_pipes,
            },
        }

        vds_plugin.run()
        present_plugin_output(vds_plugin, colorizer)

    if Config.arguments.output:
        colorizer.clean_file(Config.arguments.output)


if __name__ == '__main__':
    main()
