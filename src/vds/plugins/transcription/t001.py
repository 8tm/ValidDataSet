from pathlib import Path
from typing import Dict, List, Union


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if the "wavs" folder and transcription files exist in the dataset'
    id: str = 'T001'
    name: str = 'DatasetStructureChecker'
    released: str = '23.2.26'
    type: str = 'TranscriptionPlugin'
    version: str = '23.3.9'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'All transcription files and the wavs folder exist'
    error_message: str = 'Detected {nof} missing transcription file or "wavs" folder'
    args: Dict[str, Union[str, List[str], Dict[str, int]]]

    def run(self) -> None:
        if not isinstance(self.args['path'], str)             \
                or not isinstance(self.args['dir_name'], str) \
                or not isinstance(self.args['files'], list):
            return None

        for file in self.args['files'] + [self.args['dir_name']]:
            if not Path(self.args['path']).joinpath(file).exists():
                self.errors.append(f'{str(file):>15}')


def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
