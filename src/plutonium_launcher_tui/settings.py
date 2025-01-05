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
        print_to_log_window('Username removal failed, you cannot remove a username when you only have one username')
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

    if current_game_enum == enums.PlutoniumGames.CALL_OF_DUTY_MODERN_WARFARE_III.value:
        current_game_mode = enums.PlutoniumGameModes.MULTIPLAYER.value
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
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    if 'global_args' not in SETTINGS['global']:
        SETTINGS['global']['global_args'] = []

    save_settings()

    return SETTINGS['global']['global_args']


def set_global_args(args: list[str]):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    if 'global_args' not in SETTINGS['global']:
        SETTINGS['global']['global_args'] = []

    SETTINGS['global']['global_args']= args

    save_settings()


def add_global_arg(arg: str):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    global_args = get_global_args()

    global_args.insert(0, arg)

    set_global_args(global_args)

    save_settings()


def remove_global_arg(arg: str):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    global_args = get_global_args()

    if arg in global_args:
        global_args.remove(arg)

    SETTINGS['global']['global_args'] = global_args

    save_settings()


def get_use_staging() -> bool:
    global_settings = SETTINGS.get('global', {})

    if 'use_staging' not in global_settings:
        use_staging = False
        set_use_staging(use_staging)
        return use_staging

    use_staging = global_settings.get('use_staging')
    return bool(use_staging)


def set_use_staging(use_staging: bool):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    SETTINGS['global']['use_staging'] = use_staging

    save_settings()


def get_current_preferred_theme() -> str:
    global_settings = SETTINGS.get('global', {})
    theme = global_settings.get('theme')

    if not theme:
        theme = 'tokyo-night'
        set_current_preferred_theme(theme)

    return theme


def set_current_preferred_theme(theme: str):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    SETTINGS['global']['theme'] = theme

    save_settings()


def get_game_directory() -> str:
    default_game_dir = ''
    game_dir = default_game_dir

    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    selected_game = get_current_selected_game().value

    if selected_game not in SETTINGS['games']:
        SETTINGS['games'][selected_game] = {}
        save_settings()

    if 'game_directory' not in SETTINGS['games'][selected_game]:
        game_dir = default_game_dir
        SETTINGS['games'][selected_game]['game_directory'] = game_dir
        save_settings()
    else:
        game_dir = SETTINGS['games'][selected_game]['game_directory']
        if not os.path.isdir(game_dir) and game_dir != default_game_dir:
            # from plutonium_launcher_tui import logger
            # print_message_one = f'The following stored game directory was invalid "{game_dir}"'
            # logger.print_to_log_window(print_message_one)
            # print_message_two = f'Resetting the stored directory to default, please reselect the game directory'
            # logger.print_to_log_window(print_message_two)
            game_dir = default_game_dir
            SETTINGS['games'][selected_game]['game_directory'] = game_dir
            save_settings()

    return game_dir


def set_game_directory(game_directory: str):
    if not os.path.isdir(game_directory):
        error_message = f'The following directory you choose does not exist: "{game_directory}"'
        raise NotADirectoryError(error_message)

    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    selected_game = get_current_selected_game().value

    if selected_game not in SETTINGS['games']:
        SETTINGS['games'][selected_game] = {}

    SETTINGS['games'][selected_game]['game_directory'] = game_directory

    save_settings()



def get_game_specific_args() -> list[str]:
    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    selected_game = get_current_selected_game().value

    if selected_game not in SETTINGS['games']:
        SETTINGS['games'][selected_game] = {}

    if 'game_args' not in SETTINGS['games'][selected_game]:
        SETTINGS['games'][selected_game]['game_args'] = []

    return SETTINGS['games'][selected_game]['game_args']


def set_game_specific_args(game_args: list[str]):
    if 'games' not in SETTINGS:
        SETTINGS['games'] = {}

    selected_game = get_current_selected_game().value

    if selected_game not in SETTINGS['games']:
        SETTINGS['games'][selected_game] = {}

    SETTINGS['games'][selected_game]['game_args'] = game_args

    save_settings()


def add_game_specific_arg(game_arg: str):
    if game_arg.strip() == '':
        error_message = 'Cannot add a blank argument to the game args'
        raise RuntimeError(error_message)
    game_args = get_game_specific_args()
    game_args.append(game_arg)
    set_game_specific_args(game_args)


def remove_game_specific_arg(game_arg: str):
    game_args = get_game_specific_args()
    game_args.remove(game_arg)
    set_game_specific_args(game_args)


def get_game_mode_options():
    one = [
            ("Multiplayer", 0)
        ]
    two = [
            ("Single Player", 0),
            ("Multiplayer", 1)
        ]
    if get_current_selected_game() == enums.PlutoniumGames.CALL_OF_DUTY_MODERN_WARFARE_III.value:
        return one
    else:
        return two

def get_plutonium_appdata_dir() -> str:
    if get_use_staging():
        pluto_appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium-staging')
    else:
        pluto_appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium')
    return pluto_appdata_path


def get_plutonium_bootstrapper() -> str:
    return os.path.normpath(f'{get_plutonium_appdata_dir()}/bin/plutonium-bootstrapper-win32.exe')
