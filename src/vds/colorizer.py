import re
from pathlib import Path

from colorama import Fore, Style


class Tags:
    __dict__ = {
        'error': {
            'color': Fore.LIGHTRED_EX,
            'style': Style.BRIGHT,
        },
        'valid': {
            'color': Fore.GREEN,
            'style': Style.NORMAL,
        },
        'invalid': {
            'color': Fore.RED,
            'style': Style.NORMAL,
        },
        'warning': {
            'color': Fore.YELLOW,
            'style': Style.NORMAL,
        },
        'info': {
            'color': Fore.CYAN,
            'style': Style.NORMAL,
        },
        'file': {
            'color': Fore.LIGHTCYAN_EX,
            'style': Style.NORMAL,
        },
        'int': {
            'color': Fore.LIGHTGREEN_EX,
            'style': Style.BRIGHT,
        },
        'colon': {
            'color': Fore.LIGHTBLUE_EX,
            'style': Style.BRIGHT,
        },
    }


class Colorizer:

    def colorize(self, text: str) -> str:
        colorized_text = ''

        tags = Tags()
        full_line = ''
        for line in text.split('\n'):
            result = line
            piped_line = result.split('|')
            result = piped_line[0]

            for tag, value in tags.__dict__.items():
                regex = r'{begin}(.*?){end}'.format(begin=f'<{tag}>', end=f'<{tag}-end>')
                for match in re.findall(regex, result):
                    result = result.replace(
                        f'<{tag}>{match}<{tag}-end>',
                        f'{value["color"]}{value["style"]}{match}{Style.RESET_ALL}',
                    )

            full_line += f'{Fore.YELLOW}{Style.BRIGHT}|{Style.RESET_ALL}'.join([result] + piped_line[1:]) + '\n'

        colorized_text = full_line.replace('wavs', f'{Fore.LIGHTYELLOW_EX}{Style.DIM}wavs{Style.RESET_ALL}')
        colorized_text = colorized_text.replace('/', f'{Fore.RED}{Style.BRIGHT}/{Style.RESET_ALL}')
        colorized_text = colorized_text.replace('\\', f'{Fore.RED}{Style.BRIGHT}\\{Style.RESET_ALL}')
        return colorized_text

    @staticmethod
    def clean_file(path: Path) -> None:
        with open(path, 'r') as f:
            content = f.read()

        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        clean_text = ansi_escape.sub('', content)

        with open(path, 'w') as f:
            f.write(clean_text)
