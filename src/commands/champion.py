from bs4 import BeautifulSoup
from rich import print

from src.parsers.abilities import Abilities
from src.parsers.runes import Runes


def _parse_guide(api, champion, guide_link):
    guide_content = api.fetch_guide(champion, guide_link)
    soup = BeautifulSoup(guide_content, features='html.parser')
    # Parse runes
    runes = Runes().parse(soup)
    print(runes)
    # Parse item build
    # Parse ability order
    # Parse spells
    # Parse information


def _get_guide(api, champion):
    if champion == '':
        print('Please, select a champion first.')
        return False

    content = api.search(champion)
    bs = BeautifulSoup(content, features='html.parser')
    browse_list = bs.find('div', {'class': 'browse-list'})
    links = browse_list.find_all('a')
    link = links[0]['href']
    content = api.fetch_guide(champion, link)

    return BeautifulSoup(content, features='html.parser')


def _print_parser(app, parser):
    soup = _get_guide(app.api, app.selected_champion)
    if not soup:
        return

    response = parser.parse(soup)
    # Present runes
    print(response)


def items(app):
    pass


def runes(app):
    _print_parser(app, Runes())


def spells(app):
    pass


def abilities(app):
    _print_parser(app, Abilities())


def all_info(app):
    parsers = [
        Runes(),
        Abilities()
    ]

    for parser in parsers:
        _print_parser(app, parser)
