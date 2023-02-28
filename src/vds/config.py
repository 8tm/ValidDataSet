import argparse
from pathlib import Path
from typing import List


class Config:
    arguments: argparse.Namespace
    disabled_plugins: str = ''
    transcription_plugins_dir_path: Path = Path('transcription')
    files_plugins_dir_path: Path = Path('files')
    activate_plugins: List[str] = []


class ValidDataSetPlugin:
    pass
