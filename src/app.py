from rich.console import Console
from rich.traceback import install

from src.api import Api
from src.cache import Cache
from src.parsers.database import Database


class App:

    def __init__(self, cache_folder='cache', database_folder='database'):
        self.console = Console()
        install()
        self.cache = Cache(cache_folder)
        self.api = Api(self.cache)
        self.database = Database()
        self.database_folder = database_folder
        self.champion_names = None
        self.selected_champion = ''
        self.is_running = True

    def get_champions_names(self):
        if self.champion_names is None:
            self.champion_names = []
            with open(f'{self.database_folder}/champions.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    self.champion_names.append(line.strip().lower())

        return self.champion_names

    def quit(self):
        self.is_running = False
