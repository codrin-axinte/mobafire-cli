from bs4 import BeautifulSoup


class Database:

    def sync(self, content):
        # Parse champions and build database
        soup = BeautifulSoup(content, features='html.parser')
        divs = soup.find_all('div', attrs={'class': 'champ-list__item__name'})

        filepath = 'database/champions.txt'
        with open(filepath, 'w') as file:
            for div in divs:
                name = div.find('b')
                file.write(name.get_text() + '\n')
