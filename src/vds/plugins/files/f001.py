from pathlib import Path, PurePosixPath
from typing import Dict, List, Union

from tqdm import tqdm  # type: ignore


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if all files have been added to the transcription files'
    id: str = 'F001'
    name: str = 'WavsTranscriptionChecker'
    released: str = '23.2.26'
    type: str = 'FilePlugin'
    version: str = '23.3.9'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'All WAV files have been added to the transcription files'
    error_message: str = 'Found {nof} files that were not added to the transcript files'
    args: Dict[str, Union[str, List[str], Dict[str, int]]]

    def run(self) -> None:
        if not isinstance(self.args['path'], str) or not isinstance(self.args['dir_name'], str):
            return None

        list_of_files = list(Path(self.args['path']).joinpath(self.args['dir_name']).glob('*.wav'))
        fixed_list_of_files = []

        for file_path in list_of_files:

            fixed_list_of_files.append(str(PurePosixPath(file_path.relative_to(self.args['path']))))

        list_of_files_in_transcriptions = []

        for file_list in self.args['files']:

            list_file_path = Path(self.args['path']).joinpath(file_list)

            if not list_file_path.exists():
                continue

            for line in list_file_path.read_text(encoding='UTF-8').split('\n'):
                wav_path, *_ = line.split('|')
                list_of_files_in_transcriptions.append(str(PurePosixPath(wav_path)))

        for file in tqdm(fixed_list_of_files, total=len(fixed_list_of_files), desc=f'{self.info.name}...'):
            if file not in list_of_files_in_transcriptions:
                self.errors.append(f'{file:>44}')


def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
