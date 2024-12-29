import sys

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
        raise ValueError(f'Theme "{theme_name}" not found.')


def set_window_title(window_title:str):
    sys.stdout.write(f'\033]0;{window_title}\007')
    sys.stdout.flush()
