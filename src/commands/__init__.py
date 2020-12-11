def load_shell():
    from src.commands import champion
    from src.commands import common
    from src.shell import Shell
    shell = Shell()

    shell.add('clear', common.clear_console, ['cls'])
    shell.add('quit', common.quit_app, ['exit', 'q'])
    shell.add('debug', common.debug, ['dbg'])
    shell.add('sync', common.database_sync)
    shell.add('help', common.help)

    shell.add('all', champion.search)
    shell.add('guide', champion.search)
    shell.add('tips', champion.search)
    shell.add('counters', champion.search)
    shell.add('countered', champion.search, ['enemies'])
    shell.add('runes', champion.search)
    shell.add('items', common.command_not_implemented)
    shell.add('spells', common.command_not_implemented)

    return shell
