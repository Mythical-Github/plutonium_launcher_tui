import os
import sys
from pathlib import Path

import tomlkit

from plutonium_launcher_tui import enums

SCRIPT_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent

SETTINGS_TOML = os.path.normpath(f"{SCRIPT_DIR}/settings.toml")


if not os.path.isfile(SETTINGS_TOML):
    error_message = f'The following file was not found: "{SETTINGS_TOML}"'
    raise FileNotFoundError(error_message)

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

    if not usernames:
        usernames.append('default')
        set_usernames(usernames)

    return usernames


def set_usernames(usernames: list[str]):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    SETTINGS['global']['usernames'] = usernames

    save_settings()


def get_current_username() -> str:
    global_settings = SETTINGS.get('global', {})
    username = global_settings.get('last_selected_username')
    if not username:
        set_username('default')
    if username not in get_usernames():
        username = get_usernames()[0]
        set_username(get_usernames()[0])
    return username


def set_username(username: str):
    if 'global' not in SETTINGS:
        SETTINGS['global'] = {}

    if username not in get_usernames():
        set_usernames(get_usernames().append(username))

    SETTINGS['global']['last_selected_username'] = username

    save_settings()


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

