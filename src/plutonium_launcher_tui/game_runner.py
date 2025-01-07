import os
import subprocess

from plutonium_launcher_tui.enums import PlutoniumGameModes, PlutoniumGames
from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.settings import (
    get_current_selected_game,
    get_current_username,
    get_currently_selected_game_mode,
    get_game_directory,
    get_game_specific_args,
    get_global_args,
    get_plutonium_appdata_dir,
    get_plutonium_bootstrapper
)


def get_game_launch_arg() -> str:
    current_game_mode = get_currently_selected_game_mode()
    current_selected_game = get_current_selected_game()
    if current_selected_game == PlutoniumGames.CALL_OF_DUTY_WORLD_AT_WAR.value:
        if current_game_mode == PlutoniumGameModes.SINGLE_PLAYER:
            game_launch_arg = 't4sp'
        else:
            game_launch_arg = 't4mp'
    elif current_selected_game == PlutoniumGames.CALL_OF_DUTY_MODERN_WARFARE_III.value:
        game_launch_arg = 'iw5mp'
    if current_selected_game == PlutoniumGames.CALL_OF_DUTY_BLACK_OPS_I.value:
        if current_game_mode == PlutoniumGameModes.SINGLE_PLAYER:
            game_launch_arg = 't5sp'
        else:
            game_launch_arg = 't5mp'
    if current_selected_game == PlutoniumGames.CALL_OF_DUTY_BLACK_OPS_II.value:
        if current_game_mode == PlutoniumGameModes.SINGLE_PLAYER:
            game_launch_arg = 't6zm'
        else:
            game_launch_arg = 't6mp'
    return game_launch_arg


def run_game():
    exe = f'"{get_plutonium_bootstrapper()}"'
    exe = f'{exe} "{get_game_launch_arg()}"'
    exe = f'{exe} "{get_game_directory()}"'
    exe = f'{exe} +name'
    exe = f'{exe} {get_current_username()}'
    exe = f'{exe} -lan'
    args = [

    ]
    for arg in args:
        exe = f'{exe} {arg}'
    for arg in get_game_specific_args():
        exe = f'{exe} {arg}'
    for arg in get_global_args():
        exe = f'{exe} {arg}'

    print_to_log_window(exe)
    os.chdir(get_plutonium_appdata_dir())
    if not os.path.isdir(get_game_directory()):
        print_to_log_window(f'The following game directory is not valid "{get_game_directory()}"')
    elif not os.path.isfile(get_plutonium_bootstrapper()):
        print_to_log_window(f'The following file path is not valid "{get_plutonium_bootstrapper()}"')
    else:
        subprocess.Popen(
            exe,
            cwd=get_plutonium_appdata_dir(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
