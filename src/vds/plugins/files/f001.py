from pathlib import Path
from typing import List, Tuple

from tqdm import tqdm  # type: ignore


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if all files have been added to the transcription files'
    id: str = 'F001'
    name: str = 'WavsTranscriptionChecker'
    released: str = '23.2.26'
    type: str = 'FilePlugin'
    version: str = '23.2.26'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'All WAV files have been added to the transcription files'
    error_message: str = 'Found files that were not added to the transcript files'

    def run(self, path: Path, files: Tuple[Path], dir_name: str) -> None:
        final_messages = []

        list_of_files = list(Path(path / dir_name).glob('*.wav'))
        fixed_list_of_files = []

        for file_path in list_of_files:
            fixed_list_of_files.append(str(file_path.relative_to(path)))

        list_of_files_in_transcriptions = []

        for file_list in files:
            if not Path(path / file_list).exists():
                continue

            for line in Path(path / file_list).read_text(encoding='UTF-8').split('\n'):
                wav_path, *_ = line.split('|')
                list_of_files_in_transcriptions.append(wav_path)

        for file in tqdm(fixed_list_of_files):
            if file not in list_of_files_in_transcriptions:
                final_messages.append(f'{file:>44}')

        if final_messages:
            self.errors = [f'{self.info.id}: {self.error_message}:'] + final_messages
        self.errors = final_messages


def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
