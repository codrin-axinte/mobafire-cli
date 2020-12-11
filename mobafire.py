from sys import argv

from prompt_toolkit.styles import Style

from src.app import App
from src.commands import load_shell

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

# START CONFIGURATION
CACHE_FOLDER = 'cache'
DATABASE_FOLDER = 'database'

style = Style.from_dict({
    # User input (default text).
    '': 'white',
    # Prompt.
    'name': 'orange',
    'champion': '#00aa00',
    'pound': 'white',
    'colon': 'white',
})


# END CONFIGURATION

def main():
    # Initialize the app and the shell using the configuration data
    app = App(cache_folder=CACHE_FOLDER, database_folder=DATABASE_FOLDER)
    shell = load_shell(app=app, style=style)
    # If the app has any arguments, then iterate over all and execute each one of them as a command.
    if len(argv) > 1:
        for i in range(1, len(argv)):
            shell.execute(argv[i])
    else:
        # If no argument is supplied then we enter the interactive mode
        shell.interactive()


if __name__ == '__main__':
    main()
