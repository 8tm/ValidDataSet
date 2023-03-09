import wave
from pathlib import Path
from typing import Dict, List, Tuple, Union

from tqdm import tqdm  # type: ignore


class PluginInfo:
    author: str = 'Tadeusz Miszczyk'
    description: str = 'Check if all files are mono, 22050 Hz with length between 2 and 10 seconds'
    id: str = 'F002'
    name: str = 'WavPropertiesChecker'
    released: str = '23.3.9'
    type: str = 'FilePlugin'
    version: str = '23.3.9'


class ValidDataSetPlugin:
    info: PluginInfo = PluginInfo()
    errors: List[str] = []
    success_message: str = 'All WAV files have correct properties'
    error_message: str = 'Found {nof} files with incorrect properties'
    args: Dict[str, Union[str, List[str], Dict[str, int]]]

    @staticmethod
    def miliseconds_to_time(miliseconds: int) -> str:
        seconds, miliseconds = divmod(miliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}.{miliseconds:03d}'

    def get_details_if_invalid_properties(self, file_path: str) -> Union[Tuple[int, int, int, str], None]:
        if not isinstance(self.args['expected_properties'], Dict):
            return None

        try:
            with wave.open(file_path, 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                num_frames = wav_file.getnframes()
                duration_ms = int((num_frames / float(sample_rate)) * 1000)
                num_channels = wav_file.getnchannels()

                if num_channels > self.args['expected_properties']['number_of_channels'] \
                        or sample_rate != self.args['expected_properties']['sample_rate'] \
                        or (duration_ms < self.args['expected_properties']['min_duration']
                            or duration_ms > self.args['expected_properties']['max_duration']):
                    return num_channels, sample_rate, duration_ms, self.miliseconds_to_time(duration_ms)

        except wave.Error:
            return None
        return None

    def prepare_message(self, invalid_file_properties: Tuple[int, int, int, str]) -> str:
        if not isinstance(self.args['expected_properties'], Dict):
            return ''

        value = '{value}'
        _status_ok = f'<valid>{value}<valid-end>'
        _status_fail = f'<invalid>{value}<invalid-end>'

        channel_mode = 'mono'
        if invalid_file_properties[0] == 2:
            channel_mode = 'stereo'

        channels = _status_fail.format(value=channel_mode)
        if invalid_file_properties[0] == self.args['expected_properties']['number_of_channels']:
            channels = _status_ok.format(value=f'{channel_mode:^6}')

        sample_rate = _status_fail.format(value=f'{invalid_file_properties[1]:^5}')
        if invalid_file_properties[1] == self.args['expected_properties']['sample_rate']:
            sample_rate = _status_ok.format(value=f'{invalid_file_properties[1]:^5}')

        duration = _status_fail.format(value=invalid_file_properties[3])
        if self.args['expected_properties']['min_duration'] <= invalid_file_properties[2] \
                <= self.args['expected_properties']['max_duration']:
            duration = _status_ok.format(value=invalid_file_properties[3])

        return f'[ {channels}, {sample_rate}, {duration} ]'

    def run(self) -> None:
        wavs_dir_path = Path(str(self.args['path'])).joinpath(str(self.args['dir_name']))

        list_of_files = list(wavs_dir_path.glob('*.wav'))
        fixed_list_of_files = []

        for file_path in list_of_files:
            fixed_list_of_files.append(str(file_path.relative_to(str(self.args['path']))))

        for file, fixed_file in tqdm(
                zip(list_of_files, fixed_list_of_files), total=len(list_of_files), desc=f'{self.info.name}...',
        ):
            invalid_file_properties = self.get_details_if_invalid_properties(
                str(Path(wavs_dir_path).joinpath(file)),
            )

            if invalid_file_properties:
                self.errors.append(f'{fixed_file:>44} ' + self.prepare_message(invalid_file_properties))


def init_plugin() -> ValidDataSetPlugin:
    vds_plugin = ValidDataSetPlugin()
    return vds_plugin
