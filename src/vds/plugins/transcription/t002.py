from pathlib import Path
from typing import List, Tuple


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if there are empty lines in the transcriptions'
    id: str = 'T002'
    name: str = 'EmptyLineChecker'
    released: str = '23.2.26'
    type: str = 'TranscriptionPlugin'
    version: str = '23.2.26'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'No blank lines found in transcript files'
    error_message: str = 'An empty line was found in the transcription'

    def run(self, path: Path, files: Tuple[Path], dir_name: str) -> None:  # pylint: disable=unused-argument
        final_messages = []

        for list_file_name in files:

            if not Path(path / list_file_name).exists():
                final_messages.append(f'ERROR: FILE NOT FOUND IN DATASET: {list_file_name}')
                continue

            file_lines = list(Path(path / list_file_name).read_text(encoding='UTF-8').split('\n'))

            for line_number, line in enumerate(file_lines, start=1):
                if line_number < len(file_lines):
                    if line in ('', '\n\n'):
                        final_messages.append(f'{str(list_file_name):>15}: {line_number:>6}: <Empty Line>')
                        continue

        if final_messages:
            self.errors = [f'{self.info.id}: {self.error_message}:'] + final_messages
        self.errors = final_messages


def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
