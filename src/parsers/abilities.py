from rich.console import RenderableType
from rich.table import Table

from src.parsers.parser import Parser


class Abilities(Parser):

    def parse(self, soup) -> RenderableType:
        # 18 boxes
        # table of 18 x 4
        # champ-build__abilities__row
        divs = soup.find_all('div', attrs={'class': 'champ-build__abilities__row'})
        rows = []
        for div in divs:
            title = div.find('h4').get_text()
            span = div.find('span')
            key = ''
            if span:
                key = span.get_text()

            active = ''
            points = div.find_all('li', attrs={'class': 'lit'})
            if len(points) == 0:
                active = 'Passive'
            else:
                active = self._get_points(points)

            rows.append({
                'title': title,
                'active': active,
                'key': key
            })

        return self._get_table(rows)

    def _get_points(self, points):
        row = ''
        active = []
        max_points = 18
        max_iterations = max_points + 1

        for point in points:
            level = int(point['level'])
            active.append(level)

        for i in range(1, max_iterations):
            if i in active:
                row += str(i)
            else:
                if i > 9:
                    row += '  '
                else:
                    row += ' '
            if i < max_points:
                row += ' | '

        return row

    def _get_table(self, rows):
        table = Table(title="Abilities")

        table.add_column("Key", justify="right", style="white")
        table.add_column("Name", justify="left", style="cyan bold")
        table.add_column("Order", justify="left", style="green")

        for row in rows:
            table.add_row(row['key'], row['title'], row['active'])

        return table
