import os

from plutonium_launcher_tui.enums import PlutoniumGameModes, PlutoniumGames
from plutonium_launcher_tui.settings import get_current_selected_game, get_use_staging


def get_games_to_game_mod_args_dict():
    return {
        PlutoniumGames.CALL_OF_DUTY_WORLD_AT_WAR.value: {
            PlutoniumGameModes.SINGLE_PLAYER: 't4sp',
            PlutoniumGameModes.MULTIPLAYER: 't4mp',
        },
        PlutoniumGames.CALL_OF_DUTY_MODERN_WARFARE_III.value: {
            PlutoniumGameModes.MULTIPLAYER: 'iw5mp',
        },
        PlutoniumGames.CALL_OF_DUTY_BLACK_OPS_I.value: {
            PlutoniumGameModes.SINGLE_PLAYER: 't5sp',
            PlutoniumGameModes.MULTIPLAYER: 't5mp',
        },
        PlutoniumGames.CALL_OF_DUTY_BLACK_OPS_II.value: {
            PlutoniumGameModes.SINGLE_PLAYER: 't6zm',
            PlutoniumGameModes.MULTIPLAYER: 't6mp',
        },
    }


def get_plutonium_appdata_dir() -> str:
    if get_use_staging():
        pluto_appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium-staging')
    else:
        pluto_appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium')
    return pluto_appdata_path


def get_plutonium_bootstrapper() -> str:
    return os.path.normpath(f'{get_plutonium_appdata_dir()}/bin/plutonium-bootstrapper-win32.exe')


def get_plutonium_modern_warfare_iii_config_path_suffix() -> str:
    return 'storage/iw5/players/config_mp.cfg'


def get_plutonium_modern_warfare_iii_config_path() -> str:
    return os.path.normpath(f'{get_plutonium_appdata_dir()}/{get_plutonium_modern_warfare_iii_config_path_suffix()}')


def get_valid_plutonium_game_mode_options():
    if get_current_selected_game() == PlutoniumGames.CALL_OF_DUTY_MODERN_WARFARE_III.value:
        return [
            ("Multiplayer", 0)
        ]
    return [
        ("Single Player", 0),
        ("Multiplayer", 1)
    ]


def get_plutonium_game_selector_options():
    return [
            ("Call of Duty World at War", 0),
            ("Call of Duty Modern Warfare III", 1),
            ("Call of Duty Black Ops I", 2),
            ("Call of Duty Black Ops II", 3),
        ]


def get_all_lines_in_config(config_path: str) -> list[str]:
    with open(config_path, encoding='utf-8') as file:
        return file.readlines()


def set_all_lines_in_config(config_path: str, lines: list[str]):
    with open(config_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def add_line_to_config(config_path: str, line: str):
    if not does_config_have_line(config_path, line):
        with open(config_path, 'a', encoding='utf-8') as file:
            file.write(line + '\n')


def remove_line_from_config(config_path: str, line: str):
    lines = get_all_lines_in_config(config_path)
    with open(config_path, 'w', encoding='utf-8') as file:
        file.writelines(current_line for current_line in lines if current_line.rstrip('\n') != line)



def does_config_have_line(config_path: str, line: str) -> bool:
    return line + '\n' in get_all_lines_in_config(config_path)
