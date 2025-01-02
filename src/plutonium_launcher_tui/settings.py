import os
import sys
from pathlib import Path

import tomlkit

from plutonium_launcher_tui import enums


SCRIPT_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent

SETTINGS_TOML = os.path.normpath(f"{SCRIPT_DIR}/settings.toml")

if not os.path.isfile(SETTINGS_TOML):
    with open(SETTINGS_TOML, 'w') as file:
        file.write('')

with open(SETTINGS_TOML) as f:
    SETTINGS = tomlkit.load(f)


def save_settings():
    with open(SETTINGS_TOML, "w") as fp:
        tomlkit.dump(SETTINGS, fp)


def get_current_selected_game() -> enums.PlutoniumGames:
    global_settings = SETTINGS.get('global', {})
    last_selected_game = global_settings.get('last_selected_game')

    if last_selected_game not in enums.PlutoniumGames._value2member_map_:
        last_selected_game = enums.PlutoniumGames.CALL_OF_DUTY_WORLD_AT_WAR
        set_current_selected_game(last_selected_game)

    return last_selected_game


def set_current_selected_game(game: enums.PlutoniumGames):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    SETTINGS['global']['last_selected_game'] = game.value

    save_settings()


def get_auto_run_game():
    global_settings = SETTINGS.get('global', {})
    auto_run_game = global_settings.get('auto_run_game')

    if not auto_run_game:
        auto_run_game = False
        set_auto_run_game(auto_run_game)

    return auto_run_game


def set_auto_run_game(auto_run_game: bool):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    SETTINGS['global']['auto_run_game'] = auto_run_game

    save_settings()


def get_auto_run_game_delay():
    global_settings = SETTINGS.get('global', {})
    delay_in_seconds = global_settings.get('auto_run_game_delay')

    if not delay_in_seconds:
        delay_in_seconds = 1.0
        set_auto_run_game_delay(delay_in_seconds)

    return delay_in_seconds


def set_auto_run_game_delay(delay_in_seconds: float):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    SETTINGS['global']['auto_run_game_delay'] = delay_in_seconds

    save_settings()


def get_usernames() -> list[str]:
    global_settings = SETTINGS.get('global', {})
    usernames = global_settings.get('usernames', [])

    if not isinstance(usernames, list):
        usernames = []

    if not usernames:
        usernames = ['default']
        set_usernames(usernames)

    return usernames


def set_usernames(usernames: list[str]):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    global_settings = SETTINGS['global']
    
    if 'usernames' not in global_settings:
        global_settings['usernames'] = []

    global_settings['usernames'] = usernames

    save_settings()


def get_current_username() -> str:
    global_settings = SETTINGS.get('global', {})
    username = global_settings.get('last_selected_username')

    if not username:
        username = 'default'
        set_username(username)

    if username not in get_usernames():
        username = get_usernames()[0]
        set_username(username)

    return username


def set_username(username: str):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    if username not in get_usernames():
        current_usernames = get_usernames()
        current_usernames.append(username)
        set_usernames(current_usernames)

    SETTINGS['global']['last_selected_username'] = username

    save_settings()


def remove_username(username: str):
    usernames = get_usernames()
    if len(usernames) <= 1:
        from plutonium_launcher_tui.logger import print_to_log_window
        print_to_log_window(f'Username removal failed, you cannot remove a username when you only have one username')
        return

    if username in usernames:
        usernames.remove(username)
        set_usernames(usernames)

        current_username = get_current_username()
        if current_username == username:
            set_username(usernames[0])

        save_settings()
        from plutonium_launcher_tui.logger import print_to_log_window
        print_to_log_window(f'Username removal of username "{username}" successful')


def get_currently_selected_game_mode() -> enums.PlutoniumGameModes:
    current_game_enum = get_current_selected_game()
    current_game_string = current_game_enum.value


    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    games_settings = SETTINGS['games']

    if current_game_string not in games_settings:
        games_settings[current_game_string] = {}

    game_specific_section = games_settings[current_game_string]

    current_game_mode = game_specific_section.get('last_selected_game_mode', None)

    was_in = False
    for enum in enums.PlutoniumGameModes:
        if enum.value == current_game_mode:
            was_in = True
            break

    if not was_in:
        current_game_mode = enums.PlutoniumGameModes.SINGLE_PLAYER.value
        game_specific_section['last_selected_game_mode'] = current_game_mode
        save_settings()

    return enums.PlutoniumGameModes(current_game_mode)



def set_currently_selected_game_mode(game_mode: enums.PlutoniumGameModes):

    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    if get_current_selected_game().value not in SETTINGS['games']:
        SETTINGS['games'][get_current_selected_game().value] = {}

    SETTINGS['games'][get_current_selected_game().value]['last_selected_game_mode'] = game_mode.value

    save_settings()


def get_global_args() -> list[str]:
    return SETTINGS.get('game', 'global_args', default=[])


def set_global_args(args: list[str]):
    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    if 'global_args' not in SETTINGS['games']:
        SETTINGS['games']['global_args'] = []
    
    SETTINGS['games']['global_args'].clear()
    SETTINGS['games']['global_args'].extend(args)

    save_settings()


def add_global_arg(arg: str):
    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    global_args = get_global_args()

    global_args.append(arg)

    SETTINGS['games']['global_args'] = global_args

    save_settings()


def remove_global_arg(arg: str):
    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    global_args = get_global_args()

    if arg in global_args:
        global_args.remove(arg)

    SETTINGS['games']['global_args'] = global_args

    save_settings()


def get_use_staging():
    global_settings = SETTINGS.get('global', {})
    use_staging = global_settings.get('use_staging')

    if not use_staging:
        use_staging = False
        set_use_staging(use_staging)

    return use_staging


def set_use_staging(use_staging: bool):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    SETTINGS['global']['use_staging'] = use_staging

    save_settings()


def get_current_preferred_theme() -> str:
    global_settings = SETTINGS.get('global', {})
    theme = global_settings.get('theme')

    if not theme:
        theme = 'dracula'
        set_current_preferred_theme(theme)

    return theme


def set_current_preferred_theme(theme: str):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    SETTINGS['global']['theme'] = theme

    save_settings()


def get_game_directory():
    return


def set_game_directory():
    return


def get_game_specific_args():
    return


def set_game_specific_args():
    return


def add_game_specific_arg():
    return


def remove_game_specific_arg():
    return
