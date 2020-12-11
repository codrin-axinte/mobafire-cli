from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


class Shell:
    def __init__(self):
        self.commands = {}
        self.aliases = {}
        self.session = None

    def add(self, name, callback, aliases=None):
        self.commands[name] = callback
        if aliases is not None:
            for alias in aliases:
                self.aliases[alias] = name
        return self

    def alias(self, name, pointing_to_name):
        self.aliases[name] = pointing_to_name
        return self

    def get_function(self, command):
        if command in self.commands:
            return self.commands[command]
        elif command in self.aliases:
            return self.get_function(self.aliases[command])

        return None

    def has(self, command) -> bool:
        return self.get_function(command) is not None

    def _call(self, app, command, *args, **kwargs) -> bool:
        callback = self.get_function(command)
        if callback is not None:
            response = callback(app, *args, **kwargs)
            return True
        else:
            return False

    def setup_prompt_session(self, app, style=None):
        champions = app.get_champions_names()
        choices = self.get_prompt_choices(champions)
        completer = WordCompleter(choices)
        # Create prompt object.
        session = PromptSession()
        session.completer = completer
        session.style = style
        session.complete_in_thread = True
        session.message = self.get_prompt_message()
        self.session = session

        return self

    def execute(self, app, command):
        if command == '':
            return

        # If the command is the name of a champion, then assign and update the prompt
        if command in app.champion_names:
            app.selected_champion = command
            self.update_prompt(app.selected_champion)
            app.console.print(f'Selected champion <{command}>')
        elif self.has(command):
            if not self._call(app, command):
                app.console.log(f'[red]An error has occurred.[/red]')
        else:
            app.console.log(f'Command <{command}> not recognized.')

    def interactive(self, app):
        while app.is_running:
            command = self.session.prompt().strip().lower()
            self.execute(app, command)

    def update_prompt(self, champion):
        self.session.message = self.get_prompt_message(champion)
        return self

    @staticmethod
    def get_prompt_message(champion=''):
        return [
            ('class:name', 'mobafire'),
            ('class:colon', ':'),
            ('class:champion', champion),
            ('class:pound', '$ '),
        ]

    def get_prompt_choices(self, champions):
        choices = []
        for command in self.commands:
            choices.append(command)
        for command in self.aliases:
            choices.append(command)

        choices += champions

        return choices
