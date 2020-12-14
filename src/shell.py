from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


class Shell:
    def __init__(self, app):
        self.app = app
        self.commands = {}
        self.aliases = {}
        self.session = None

    def add(self, command, callback, aliases=None):
        self.commands[command] = callback
        if aliases is not None:
            for alias in aliases:
                self.aliases[alias] = command
        return self

    def alias(self, name, command):
        self.aliases[name] = command
        return self

    def has(self, command) -> bool:
        return self._get_function_pointer(command) is not None

    def setup_prompt_session(self, style=None):
        champions = self.app.get_champions_names()
        choices = self._get_prompt_choices(champions)
        completer = WordCompleter(choices)
        # Create prompt object.
        session = PromptSession()
        session.completer = completer
        session.style = style
        session.complete_in_thread = True
        session.message = self._get_prompt_message()
        self.session = session

        return self

    def run(self, argv):
        # If the app has any arguments, then iterate over all and execute each one of them as a command.
        if len(argv) > 1:
            for i in range(1, len(argv)):
                self.execute(argv[i])
        else:
            # If no argument is supplied then we enter the interactive mode
            self.interactive()

    def execute(self, command):
        """
        Find the callable function based on the given command name and then call it.
        This method will search within the commands and aliases dictionaries.
        :param command:
        :return:
        """

        # Do nothing, my man needs some space
        if command == '':
            return

        # If the command is the name of a champion,
        # then assign the champion and update the prompt
        if command in self.app.champion_names:
            self.app.selected_champion = command
            self.session.message = self._get_prompt_message(self.app.selected_champion)
            self.app.console.print(f'Selected champion <{command}>')

        # Even though we can remove the has check and use only the _call method,
        # We separate them so we can have more control over the feedback we give to the user.
        elif self.has(command):
            if not self._call(command):
                self.app.console.log(f'[red]An error has occurred.[/red]')
        else:
            self.app.console.log(f'[red]Command <{command}> not recognized.[/red]')

    def interactive(self):
        """
        The interactive mode is continuous way to execute commands,
        Until the user decides to close the session.
        :param app:
        :return:
        """
        while self.app.is_running:
            command = self.session.prompt().strip().lower()
            self.execute(command)

    def _get_function_pointer(self, command):

        if command in self.commands:
            return self.commands[command]
        elif command in self.aliases:
            # We do it recursively in case we have nested pointers.
            # Example: exit -> q -> quit
            # This shouldn't happen though, but just in case.
            return self._get_function_pointer(self.aliases[command])

        return None

    def _call(self, command) -> bool:
        callback_pointer = self._get_function_pointer(command)
        if callback_pointer is not None:
            response = callback_pointer(self.app)
            return True
        else:
            return False

    @staticmethod
    def _get_prompt_message(champion=''):
        return [
            ('class:name', 'mobafire'),
            ('class:colon', ':'),
            ('class:champion', champion),
            ('class:pound', '$ '),
        ]

    def _get_prompt_choices(self, champions):
        choices = []
        for command in self.commands:
            choices.append(command)
        for command in self.aliases:
            choices.append(command)

        choices += champions

        return choices
