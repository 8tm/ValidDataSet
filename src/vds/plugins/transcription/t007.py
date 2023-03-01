from pathlib import Path
from typing import Dict, List, Tuple, Union


class BaseMeta(type):
    files: Dict[str, List[Tuple[str, int, str, str]]] = {}

    def __getitem__(cls, key: str) -> str:
        return getattr(cls, key)

    def __setattr__(cls, name: str, value: str) -> None:
        setattr(cls, name, value)

    def add_file_to_dict(cls, file_path: str, line_number: int, wav_path: str, transcription: str) -> None:
        file_name = str(wav_path)
        if file_name not in cls.files:
            cls.files[file_name] = []
        cls.files[file_name].append((file_path, line_number, wav_path, transcription))


class Duplicates(metaclass=BaseMeta):
    files: Dict[str, List[Tuple[Path, int, str, str]]] = {}


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if there are any duplicate paths to WAV files in the transcriptions'
    id: str = 'T007'
    name: str = 'DuplicatedTranscriptionChecker'
    released: str = '23.2.26'
    type: str = 'TranscriptionPlugin'
    version: str = '23.3.9'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'No duplicated paths to WAV files found in transcriptions'
    error_message: str = 'Found {nof} duplicated path to the WAV file in transcription file'
    args: Dict[str, Union[str, List[str], Dict[str, int]]]

    def run(self) -> None:
        if not isinstance(self.args['path'], str):
            return None

        final_messages = []

        for list_file_name in self.args['files']:

            list_file_path = Path(self.args['path']).joinpath(list_file_name)

            if not list_file_path.exists():
                final_messages.append(f'ERROR: FILE NOT FOUND IN DATASET: {list_file_name}')
                continue

            file_lines = list(list_file_path.read_text(encoding='UTF-8').split('\n'))

            for line_number, line in enumerate(file_lines, start=1):

                if line in ('', '\n\n'):
                    continue
                wav_path, *transcription = line.split('|')
                Duplicates.add_file_to_dict(list_file_name, line_number, wav_path, '|'.join(transcription))

        for _, duplicate in Duplicates.files.items():

            if len(duplicate) > 1:
                full_message = ''

                for entry_index, entry in enumerate(duplicate, start=1):

                    message = f'<file>{str(entry[0]):>15}<file-end>' \
                              f'<colon>: <colon-end>'                \
                              f'<int>{entry[1]:>6}<int-end>'         \
                              f'<colon>: <colon-end>'                \
                              f'{entry[2]}|{entry[3]}'
                    replace_text = (
                        (str(entry[0]), str(entry[0])),
                        (str(entry[1]), str(entry[1])),
                    )

                    for elements in replace_text:
                        message = message.replace(*elements)

                    full_message += f'{message}\n' if entry_index < len(duplicate) else message

                self.errors.append(full_message)


def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
