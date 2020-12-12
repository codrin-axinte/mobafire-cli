from pathlib import Path

from rich.columns import Columns
from rich.console import RenderableType
from rich.panel import Panel

from src.parsers.parser import Parser


class Runes(Parser):

    def parse(self, soup) -> RenderableType:
        runes = soup.find_all('div', attrs={'class': 'new-runes'})
        rune = runes[0]
        types = ['primary', 'secondary', 'bonuses']
        columns = [self.get_path(rune, runeType) for runeType in types]
        return Columns(columns)

    def get_path(self, rune, path):
        div = rune.find('div', attrs={'class': f'new-runes__{path}'})
        images = div.find_all('img')
        colors = {'primary': 'red', 'secondary': 'blue', 'bonuses': 'magenta'}
        color = colors.get(path)
        content = ''
        for img in images:
            name = Path(img['src']).stem
            content += name.capitalize() + '\n'

        return Panel.fit(content, title=f'[bold {color}]{path.upper()}[/bold {color}]')
