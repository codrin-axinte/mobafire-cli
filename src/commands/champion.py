from bs4 import BeautifulSoup
from src.parsers.runes import Runes
from rich import print


def _parse_guide(api, champion, guide_link):
    guide_content = api.fetch_guide(champion, guide_link)
    soup = BeautifulSoup(guide_content, features='html.parser')
    # Parse runes
    runes = Runes().get(soup)
    print(runes)
    # Parse item build
    # Parse ability order
    # Parse spells
    # Parse information


def search(app):
    if app.selected_champion == '':
        print('Please, select a champion first.')
        return True

    champion = app.selected_champion
    api = app.api
    content = api.search(champion)
    bs = BeautifulSoup(content, features='html.parser')
    browse_list = bs.find('div', {'class': 'browse-list'})
    links = browse_list.find_all('a')
    guide_link = links[0]['href']
    _parse_guide(api, champion, guide_link)

    return True

