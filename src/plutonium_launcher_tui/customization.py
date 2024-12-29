import os
import sys
from shutil import get_terminal_size

from textual.app import App
from textual.theme import ThemeProvider


def set_theme(app_instance: App, theme_name: str):
    theme_found = False

    for name, callback in ThemeProvider(app_instance).commands:
        if name == theme_name:
            callback()
            theme_found = True
            break

    if not theme_found:
        error_message = f'Theme "{theme_name}" not found.'
        raise ValueError(error_message)


def set_terminal_size(x: int, y: int):
    os.system(f'mode con: cols={x} lines={y}')


def set_window_title(window_title: str):
    os.system(f'tit;e {window_title}')



# def set_window_title(window_title: str):
#     sys.stdout.write(f"\033]0;{window_title}\007")
#     sys.stdout.flush()
