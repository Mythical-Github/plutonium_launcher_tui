from plutonium_launcher_tui.screens import text_input_screen
from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.settings import (
    get_game_specific_args,
    add_game_specific_arg
)


class GameArgsScreen(text_input_screen.TextInputScreen):
    def __init__(self):
        super().__init__(
            cancel_function=self.cancel,
            confirm_function=self.confirm,
            input_name="game argument"
        )

    def cancel(self, text_input):
        print_to_log_window('The cancel button was pressed')

    def confirm(self, text_input):
        text_value = text_input.value
        if not text_value or text_value.strip() == '':
            print_to_log_window('You cannot add a blank argument')
        elif text_value in get_game_specific_args():
            print_to_log_window('You cannot add a game argument that already exists')
        else:
            add_game_specific_arg(text_value)
