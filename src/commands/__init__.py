def load_shell(app, style):
    from src.commands import champion
    from src.commands import common
    from src.shell import Shell

    shell = Shell(app)

    # Global Commands
    shell.add('clear', common.clear_console, ['cls'])
    shell.add('quit', common.quit_app, ['exit', 'q'])
    shell.add('debug', common.debug, ['dbg'])
    shell.add('db:sync', common.database_sync)
    shell.add('cache:clear', common.cache_clear)
    shell.add('help', common.help)

    # Champion Commands
    shell.add('all', champion.all_info)
    shell.add('guide', common.command_not_implemented)
    shell.add('tips', common.command_not_implemented)
    shell.add('counters', common.command_not_implemented)
    shell.add('countered', common.command_not_implemented, ['enemies'])
    shell.add('runes', champion.runes)
    shell.add('abilities', champion.abilities, ['skills'])
    shell.add('items', champion.items)
    shell.add('spells', common.command_not_implemented)

    # Setup shell prompt
    shell.setup_prompt_session(style)

    return shell
