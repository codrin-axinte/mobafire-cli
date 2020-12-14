def command_not_implemented(app):
    from rich import print
    print('This command is recognized but is not yet implemented.')
    return True


def database_sync(app):
    content = app.api.fetch_champions()
    app.database.sync(content)


def debug(app):
    from bs4 import BeautifulSoup
    from src.parsers.runes import Runes
    from rich import print
    content = app.cache.read('dump.html')
    soup = BeautifulSoup(content, features='html.parser')
    runes = Runes().parse(soup)
    print(runes)


def cache_clear(app):
    app.cache.reload()


def quit_app(app):
    app.quit()


def clear_console(app):
    app.console.clear()


def help(app):
    command_not_implemented(app)
