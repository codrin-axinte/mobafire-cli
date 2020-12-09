from bs4 import BeautifulSoup
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.traceback import install

from src.api import Api
from src.cache import Cache
from src.parsers.database import Database
from src.parsers.runes import Runes

'''

Documentation References:

Beautiful Soup: 
    - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
Rich: 
    - https://github.com/willmcgugan/rich
    - https://rich.readthedocs.io/en/latest/prompt.html
    
Prompt Toolkit:
    - https://github.com/prompt-toolkit/python-prompt-toolkit
    - https://python-prompt-toolkit.readthedocs.io/en/stable/pages/progress_bars.html
    
Mobafire: 
    - https://www.mobafire.com/

'''

kb = KeyBindings()
console = Console()
install()
cache = Cache('cache')
api = Api(cache)
database = Database()

style = Style.from_dict({
    # User input (default text).
    '': 'white',
    # Prompt.
    'name': 'orange',
    'pound': 'white',
})

PROMPT = [
    ('class:name', 'mobafire'),
    ('class:pound', '$ '),
]


def sync():
    content = api.fetch_champions()
    database.sync(content)


def get_prompt_choices():
    choices = [
        'quit',
        'exit',
        'q',
        'debug',
        'dbg',
        'clear',
        'cls',
        'sync'
    ]

    with open('database/champions.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            choices.append(line.strip().lower())

    return choices


def parse_guide(champion, guide_link):
    guide_content = api.fetch_guide(champion, guide_link)
    soup = BeautifulSoup(guide_content, features='html.parser')
    # Parse runes
    runes = Runes().get(soup)
    console.print(runes)
    # Parse item build
    # Parse ability order
    # Parse spells
    # Parse information


def search(champion):
    content = api.search(champion)
    bs = BeautifulSoup(content, features='html.parser')
    browse_list = bs.find('div', {'class': 'browse-list'})
    links = browse_list.find_all('a')
    guide_link = links[0]['href']
    parse_guide(champion, guide_link)


def debug(filepath='cache/dump.html'):
    with open(filepath, 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, features='html.parser')
        runes = Runes().get(soup)
        console.print(runes)


@kb.add('c-space')
def _(event):
    " Initialize autocompletion, or select the next completion. "
    buff = event.app.current_buffer
    if buff.complete_state:
        buff.complete_next()
    else:
        buff.start_completion(select_first=False)


def init_prompt():
    choices = get_prompt_choices()
    completer = WordCompleter(choices)
    # Create prompt object.
    session = PromptSession()
    session.completer = completer
    session.style = style
    session.complete_in_thread = True
    session.key_bindings = kb
    session.message = PROMPT
    return session


def main():
    keep_alive = True
    session = init_prompt()

    while keep_alive:
        cmd = session.prompt().strip().lower()

        if cmd == '':
            continue

        if cmd in ['quit', 'exit', 'q']:
            keep_alive = False
        elif cmd in ['debug', 'dbg']:
            debug()
        elif cmd in ['clear', 'cls']:
            console.clear()
        elif cmd == 'sync':
            sync()
        else:
            search(cmd)


if __name__ == '__main__':
    main()
    # debug()
