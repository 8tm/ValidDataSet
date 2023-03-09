from pathlib import Path
from typing import Dict, List, Union


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if all lines have the same number of PIPE characters'
    id: str = 'T006'
    name: str = 'PunctuationMarksChecker'
    released: str = '23.2.26'
    type: str = 'TranscriptionPlugin'
    version: str = '23.3.9'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'All PIPE characters used in the translation files are in the same quantity'
    error_message: str = 'The PIPE symbol has been used more times than the default setting allows ' \
                         '(in {nof} transcriptions)'
    args: Dict[str, Union[str, List[str], Dict[str, int]]]

    def run(self) -> None:
        if not isinstance(self.args['path'], str) or not isinstance(self.args['expected_properties'], dict):
            return None

        for list_file_name in self.args['files']:

            list_file_path = Path(self.args['path']).joinpath(list_file_name)

            if not list_file_path.exists():
                self.errors.append(f'<invalid>ERROR: FILE NOT FOUND IN DATASET: {list_file_name}<invalid-end>')
                continue

            file_lines = list(list_file_path.read_text(encoding='UTF-8').split('\n'))

            for line_number, line in enumerate(file_lines, start=1):

                if line in ('', '\n\n'):
                    continue

                pipes_number = line.count('|')

                if pipes_number > int(self.args['expected_properties']['number_of_pipes']):
                    self.errors.append(
                        f'<file>{str(list_file_name):>15}<file-end>'
                        f'<colon>: <colon-end>'
                        f'<int>{line_number:>6}<int-end>'
                        f'<colon>: <colon-end>'
                        f'{line}',
                    )


def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
