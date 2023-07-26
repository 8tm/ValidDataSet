import wave
from pathlib import Path
from typing import Dict, List, Tuple, Union

from tqdm import tqdm  # type: ignore

from scipy.io.wavfile import read, WavFileWarning
import warnings
warnings.filterwarnings("error", category=WavFileWarning)

class PluginInfo:
    author: str = 'Patryk Gensch'
    description: str = 'Check if all wav files will not throw WavFileWarning on load or they don\'t have other errors'
    id: str = 'F003'
    name: str = 'WavCorrectnessChecker'
    released: str = '23.4.2'
    type: str = 'FilePlugin'
    version: str = '23.4.2'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'All WAV files are correct'
    error_message: str = 'Found {nof} files with problems'
    args: Dict[str, Union[str, List[str], Dict[str, int]]]

    def format_message(self, err_type):
        value = '{value}'
        _status_ok = f'<valid>{value}<valid-end>'
        _status_warning = f'<warning>{value}<warning-end>'
        _status_fail = f'<invalid>{value}<invalid-end>'

        status = "{unknown}"

        if err_type is None:
            status = _status_ok.format(value='OK')
        else:
            if err_type == 0:
                status = _status_fail.format(value='is not a WAV file')
            elif err_type == 1:
                status = _status_warning.format(value='has metadata (exported from Audacity?)')
            elif err_type == 2:
                status = _status_fail.format(value='truncated')
            elif err_type == 3:
                status = _status_fail.format(value='unknown, but error')

        return f'[{status}]'

    def run(self) -> None:
        wavs_dir_path = Path(str(self.args['path'])).joinpath(str(self.args['dir_name']))

        list_of_files = list(wavs_dir_path.glob('*.wav'))
        fixed_list_of_files = []

        for file_path in list_of_files:
            fixed_list_of_files.append(str(file_path.relative_to(str(self.args['path']))))

        for file, fixed_file in tqdm(
                zip(list_of_files, fixed_list_of_files), total=len(list_of_files), desc=f'{self.info.name}...',
        ):
            try:
                _ = read(file)
            except WavFileWarning as e:
                msg = str(e)
                if msg.__contains__("Chunk (non-data) not understood, skipping it."):
                    self.errors.append(f'{fixed_file:>44} ' + self.format_message(1))
                    continue
                elif msg.__contains__("Reached EOF prematurely"):
                    self.errors.append(f'{fixed_file:>44} ' + self.format_message(2))
                    continue
                else:
                    self.errors.append(f'{fixed_file:>44} ' + self.format_message(3))
                    continue
            except:
                self.errors.append(f'{fixed_file:>44} ' + self.format_message(0))
                continue

def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
