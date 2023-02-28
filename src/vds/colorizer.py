import re

from colorama import Fore, Style


class NumbersConfig:
    color: str = Fore.LIGHTGREEN_EX
    style: str = Style.BRIGHT
    regex: str = r'(?:^|\s)(\d+|[0-9]*\.[0-9]+)\D'


class IdConfig:
    color: str = Fore.LIGHTRED_EX
    style: str = Style.BRIGHT
    regex: str = r'([TF][0-9]{3})(?=[\s,: ]|$)'


class PIPEConfig:
    color: str = Fore.YELLOW
    style: str = Style.BRIGHT
    regex: str = r'\|'


class SlashConfig:
    color: str = Fore.RED
    style: str = Style.DIM
    regex: str = r'[\\/]'


class FileConfig:
    color: str = Fore.LIGHTCYAN_EX
    style: str = Style.NORMAL
    regex: str = r'(\S+)\.(\S+)\:'


class ColonConfig:
    color: str = Fore.LIGHTBLUE_EX
    style: str = Style.BRIGHT
    regex: str = r':'


class Colorizer:
    numbers: NumbersConfig = NumbersConfig()
    id: IdConfig = IdConfig()
    pipe: PIPEConfig = PIPEConfig()
    slash: SlashConfig = SlashConfig()
    file: FileConfig = FileConfig()
    colon: ColonConfig = ColonConfig()

    def colorize(self, text: str) -> str:
        colorized_text = ''
        for line in text.split('\n'):
            piped_line = line.split('|')

            new_line = piped_line[0]

            result = re.sub(
                self.numbers.regex, self.numbers.color + self.numbers.style + r'\g<0>' + Style.RESET_ALL, new_line,
            )
            result = re.sub(
                self.id.regex, self.id.color + self.id.style + r'\g<0>' + Style.RESET_ALL, result,
            )
            result = re.sub(
                self.pipe.regex, self.pipe.color + self.pipe.style + r'\g<0>' + Style.RESET_ALL, result,
            )
            result = re.sub(
                self.slash.regex, self.slash.color + self.slash.style + r'\g<0>' + Style.RESET_ALL, result,
            )
            result = re.sub(
                self.file.regex, self.file.color + self.file.style + r'\g<0>' + Style.RESET_ALL, result,
            )
            result = re.sub(
                self.colon.regex, self.colon.color + self.colon.style + r'\g<0>' + Style.RESET_ALL, result,
            )

            colorized_text += f'{Fore.YELLOW}{Style.BRIGHT}|{Style.RESET_ALL}'.join([result] + piped_line[1:]) + '\n'
        return colorized_text
