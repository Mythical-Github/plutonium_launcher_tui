from plutonium_launcher_tui.screens import text_input_screen
from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.settings import get_usernames, set_username


class UsernameScreen(text_input_screen.TextInputScreen):
    def __init__(self):
        super().__init__(
            cancel_function=self.simulate_cancel_username_button_pressed,
            confirm_function=self.simulate_confirm_username_button_pressed,
            input_name="username"
        )

    def simulate_cancel_username_button_pressed(self, text_input):
        print_to_log_window('The cancel button was pressed')

    def simulate_confirm_username_button_pressed(self, text_input):
        text_value = text_input.value

        if not text_value or text_value.strip() == '':
            print_to_log_window('You cannot add a blank username')
        elif text_value in get_usernames():
            print_to_log_window('You cannot add a username that already exists')
        else:
            set_username(text_value)
