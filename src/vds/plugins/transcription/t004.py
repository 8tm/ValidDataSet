import string
from pathlib import Path
from typing import Dict, List, Union


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if all files added to transcription have a transcription'
    id: str = 'T004'
    name: str = 'ExistingWavFileTranscriptionChecker'
    released: str = '23.2.26'
    type: str = 'TranscriptionPlugin'
    version: str = '23.3.9'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'All WAV files added to the transcription files have a transcription'
    error_message: str = 'Found {nof} empty transcription'
    args: Dict[str, Union[str, List[str], Dict[str, int]]]

    def run(self) -> None:
        if not isinstance(self.args['path'], str):
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

                _, *transcription = line.split('|')
                text = '|'.join(transcription)

                if len(text.translate(str.maketrans('', '', string.punctuation + ' '))) == 0:
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
