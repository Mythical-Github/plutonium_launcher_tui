import os

import pygetwindow
from textual.app import App

# from textual.theme import ThemeProvider


# def set_theme(app_instance: App, theme_name: str):
#     theme_found = False

#     for name, callback in ThemeProvider(app_instance).commands:
#         if name == theme_name:
#             callback()
#             theme_found = True
#             break

#     if not theme_found:
#         error_message = f'Theme "{theme_name}" not found.'
#         raise ValueError(error_message)


def set_terminal_size(app: App, x: int, y: int):
    all_windows = pygetwindow.getAllWindows()

    # make this an equality check and not a substring check later
    windows = [win for win in all_windows if app.TITLE in win.title]

    for window in windows:
        try:
            window.resizeTo(x, y)
            # print(f"Resized window: {window.title} to {x}x{y}")
        except Exception as e:
            e


def set_window_title(window_title: str):
    os.system(f'title {window_title}')


# def set_window_title(window_title: str):
#     sys.stdout.write(f"\033]0;{window_title}\007")
#     sys.stdout.flush()


# def set_terminal_font_size(font_size: int):
#     return
