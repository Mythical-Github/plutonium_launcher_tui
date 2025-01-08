import os

from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.screens import text_input_screen
from plutonium_launcher_tui.settings import get_current_selected_game, set_game_directory


class GameDirectoryScreen(text_input_screen.TextInputScreen):
    def __init__(self, widget_to_refresh=None):
        super().__init__(
            cancel_function=self.cancel,
            confirm_function=self.confirm,
            input_name="game directory",
            widget_to_refresh=widget_to_refresh
        )
        self.widget_to_refresh = widget_to_refresh

    def cancel(self, text_input):
        print_to_log_window('The cancel button was pressed')

    def confirm(self, text_input):
        print_to_log_window('The confirm button was pressed')
        dir_path = os.path.normpath(str(text_input.value).strip().strip('"').strip("'"))

        if not os.path.isdir(dir_path) or dir_path == '.':
            is_not_a_dir_message = f'The following provided directory is invalid: "{dir_path}"'
            print_to_log_window(is_not_a_dir_message)
        else:
            is_a_dir_message = f'The following provided directory: "{dir_path}" was set for the following game: "{get_current_selected_game()}"'
            set_game_directory(dir_path)
            print_to_log_window(is_a_dir_message)
