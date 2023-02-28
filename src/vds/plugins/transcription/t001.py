from pathlib import Path
from typing import List, Tuple


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if the "wavs" folder and transcription files exist in the dataset'
    id: str = 'T001'
    name: str = 'DatasetStructureChecker'
    released: str = '23.2.26'
    type: str = 'TranscriptionPlugin'
    version: str = '23.2.26'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'All transcription files and the wavs folder exist'
    error_message: str = 'Detected missing transcription file or "wavs" folder'

    def run(self, path: Path, files: Tuple[Path], dir_name: str) -> None:
        final_messages = []

        for file in (dir_name,) + files:
            if not (Path(path) / str(file)).exists():
                final_messages.append(f'{str(file):>15}')

        if final_messages:
            self.errors = [f'{self.info.id}: {self.error_message}:'] + final_messages
        self.errors = final_messages


def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
