import os
import subprocess
import webbrowser

import textual.keys
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Checkbox, Header, Input, Select, Static
from textual_spinbox import SpinBox

from plutonium_launcher_tui import enums
from plutonium_launcher_tui.base_widgets import (
    BasePlutoniumLauncherButton,
    BasePlutoniumLauncherHorizontalBox,
    BasePlutoniumLauncherLabel,
)
from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.settings import (
    add_global_arg,
    get_auto_run_game,
    get_auto_run_game_delay,
    get_current_selected_game,
    get_current_username,
    get_currently_selected_game_mode,
    get_game_directory,
    get_global_args,
    get_use_staging,
    get_usernames,
    set_current_selected_game,
    set_currently_selected_game_mode,
    set_username,
    get_game_specific_args,
    add_game_specific_arg,
    set_use_staging,
    set_auto_run_game
)


def open_directory_in_file_browser(directory_path: str):
    if os.path.isdir(directory_path):
        program = "explorer"
        subprocess.run([program, directory_path], check=False)
        print_to_log_window(f'Opening the following directory in the file browser: "{directory_path}"')
    else:
        print_to_log_window(f'The specified path is not a directory: "{directory_path}"')


def open_website(url: str):
    print_to_log_window(f"Opening website url: {url}")
    try:
        webbrowser.open(url, new=2)
    except RuntimeError as error_message:
        print_to_log_window(f"An error occurred: {error_message!s}")


class AddGlobalArgButton(Static):
    def compose(self) -> ComposeResult:
        self.add_global_arg_button = BasePlutoniumLauncherButton(button_text="+", button_width="auto")
        yield self.add_global_arg_button

    def on_mount(self):
        self.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        from plutonium_launcher_tui.main_app import app
        app.global_args_screen.refresh(recompose=True)
        app.push_screen(app.global_args_screen)


def allow_global_args_blank() -> bool:
    if len(get_global_args()) == 0:
        return True
    else:
        return False


class RemoveGlobalArgButton(Static):
    def compose(self) -> ComposeResult:
        self.remove_button = BasePlutoniumLauncherButton(button_text="-", button_width="auto")
        yield self.remove_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.remove_button.styles.height = "auto"
        self.remove_button.styles.text_align = "center"
        self.remove_button.styles.align = ("center", "middle")
        self.remove_button.styles.content_align = ("center", "middle")

    def on_button_pressed(self) -> None:
        from plutonium_launcher_tui.main_app import app
        from plutonium_launcher_tui.settings import remove_global_arg

        options = app.global_args_section.options

        if not len(options) > 0:
            return

        global_arg = options[app.global_args_section.combo_box.value][0]

        print_to_log_window(f'Attempting to remove the following global argument: "{global_arg}"')
        remove_global_arg(global_arg)
        app.global_args_section.refresh(recompose=True)


class PlutoniumGlobalArgsSection(Static):
    def compose(self) -> ComposeResult:

        self.options = []

        for arg_index, arg in enumerate(get_global_args()):
            self.options.append((arg, arg_index))


        self.combo_box: Select[int] = Select(self.options, allow_blank=allow_global_args_blank(), prompt='None')

        self.add_button = AddGlobalArgButton()

        self.remove_button = RemoveGlobalArgButton()

        with BasePlutoniumLauncherHorizontalBox():
            yield BasePlutoniumLauncherLabel(label_text="Global Args:", label_height="auto")
            yield self.combo_box
            yield self.remove_button
            yield self.add_button


class AddGameArgButton(Static):
    def compose(self) -> ComposeResult:
        self.add_game_arg_button = BasePlutoniumLauncherButton(button_text="+", button_width="auto")
        yield self.add_game_arg_button

    def on_mount(self):
        self.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        from plutonium_launcher_tui.main_app import app
        app.global_args_screen.refresh(recompose=True)
        app.push_screen(app.game_args_screen)


class RemoveGameArgButton(Static):
    def compose(self) -> ComposeResult:
        self.remove_button = BasePlutoniumLauncherButton(button_text="-", button_width="auto")
        yield self.remove_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.remove_button.styles.height = "auto"
        self.remove_button.styles.text_align = "center"
        self.remove_button.styles.align = ("center", "middle")
        self.remove_button.styles.content_align = ("center", "middle")

    def on_button_pressed(self) -> None:
        from plutonium_launcher_tui.main_app import app
        from plutonium_launcher_tui.settings import remove_game_specific_arg

        options = app.game_args_section.options

        if not len(options) > 0:
            return

        game_arg = options[app.game_args_section.combo_box.value][0]

        print_to_log_window(f'Attempting to remove the following game specific argument: "{game_arg}"')
        remove_game_specific_arg(game_arg)
        app.game_args_section.refresh(recompose=True)


def allow_game_args_blank() -> bool:
    if len(get_game_specific_args()) == 0:
        return True
    else:
        return False


class PlutoniumGameSpecificArgsSection(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()

        self.options = []

        for arg_index, arg in enumerate(get_game_specific_args()):
            self.options.append((arg, arg_index))

        self.combo_box: Select[int] = Select(self.options, allow_blank=allow_game_args_blank(), prompt='None')

        self.game_args_label = BasePlutoniumLauncherLabel(label_text="Game Args:", label_height="auto")

        self.add_button = AddGameArgButton()

        self.remove_button = RemoveGameArgButton()

        with self.horizontal_box:
            yield self.game_args_label
            yield self.combo_box
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box

    def on_mount(self):
        self.game_args_label.styles.height = "auto"


def generate_spinbox_numbers():
    current = 0
    max_num = 999
    while current <= (max_num + 1):
        yield round(current, 1)
        current += 0.1


class AutoRunGameCheckBox(Static):
    def compose(self) -> ComposeResult:
        self.checkbox = Checkbox(value=get_auto_run_game())
        yield self.checkbox

    def on_mount(self):
        self.styles.width = 'auto'

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        set_auto_run_game(event.value)
        check_box_changed_message = f'{event.value}'
        print_to_log_window(check_box_changed_message)


class StagingCheckBox(Static):
    def compose(self) -> ComposeResult:
        self.checkbox = Checkbox(value=get_use_staging())
        yield self.checkbox

    def on_mount(self):
        self.styles.width = 'auto'


    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        set_use_staging(event.value)
        check_box_changed_message = f'{event.value}'
        print_to_log_window(check_box_changed_message)


class PlutoniumGameAutoExecuteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox(width="100%")
        with self.horizontal_box:
            self.auto_execute_label = BasePlutoniumLauncherLabel(
                "Auto Run Game:",
                label_content_align=("left", "middle"),
                label_width="auto"
            )
            self.auto_execute_checkbox = AutoRunGameCheckBox()
            self.auto_execute_delay_label = BasePlutoniumLauncherLabel(
                "Delay:",
                label_content_align=("left", "middle"),
                label_width="auto"
            )
            self.auto_execute_delay_spin_box = SpinBox(iter_val=list(generate_spinbox_numbers()), init_val=get_auto_run_game_delay())
            self.staging_label = BasePlutoniumLauncherLabel(
                "Use Staging:",
                label_content_align=("left", "middle"),
                label_width="auto"
            )
            self.staging_checkbox = StagingCheckBox()
            yield self.staging_label
            yield self.staging_checkbox
            yield self.auto_execute_label
            yield self.auto_execute_checkbox
            yield self.auto_execute_delay_label
            yield self.auto_execute_delay_spin_box

    def on_mount(self):
        self.auto_execute_delay_spin_box.styles.width = "1fr"
        self.auto_execute_checkbox.styles.width = 'auto'
        self.auto_execute_checkbox.styles.content_align = ("center", "middle")
        self.staging_checkbox.styles.width = 'auto'


class SelectGameDirectoryButton(Static):
    def compose(self) -> ComposeResult:
        self.select_game_directory_button = BasePlutoniumLauncherButton(
                button_text="··",
                button_width='6',
                button_border=("none", "black")
            )
        yield self.select_game_directory_button

    def on_mount(self):
        self.styles.width = '6'
        self.select_game_directory_button.styles.padding = 0
        self.select_game_directory_button.styles.margin = 0


    def on_button_pressed(self) -> None:
        from plutonium_launcher_tui.main_app import app
        app.global_args_screen.refresh(recompose=True)
        app.push_screen(app.game_directory_screen)


class PlutoniumGameDirectoryBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        with self.horizontal_box:
            self.game_dir_label = BasePlutoniumLauncherLabel("Game Directory:")
            self.game_dir_location_label = BasePlutoniumLauncherLabel(get_game_directory())
            self.select_dir_button = SelectGameDirectoryButton()
            yield self.game_dir_label
            yield self.game_dir_location_label
            yield self.select_dir_button

    def on_mount(self):
        self.horizontal_box.styles.width = '100%'
        self.styles.width = '100%'
        self.game_dir_location_label.styles.height = "3"
        self.game_dir_location_label.styles.width = '1fr'
        self.game_dir_location_label.styles.content_align = ("left", "middle")
        self.game_dir_location_label.styles.text_align = "left"
        self.game_dir_location_label.styles.align = ("left", "middle")
        self.select_dir_button.styles.text_align = "center"
        self.select_dir_button.styles.align = ("center", "middle")
        self.select_dir_button.styles.content_align = ("center", "middle")
        self.select_dir_button.styles.height = "auto"


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


class PlutoniumGameModeSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        self.game_mode_label = BasePlutoniumLauncherLabel("Game Mode:")

        # generate this from the enum later
        self.options = get_game_mode_options()

        main_value = None
        current_game = get_currently_selected_game_mode().value

        for entry in self.options:
            if entry[0] == current_game:
                main_value = entry[1]
                break
            else:
                error_message = 'The currently selected game is invalid.'
                RuntimeWarning(error_message)

        self.my_select: Select[int] = Select(self.options, allow_blank=False, value=main_value)
        with self.horizontal_box:
            yield self.game_mode_label
            yield self.my_select


    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        set_currently_selected_game_mode(enums.get_enum_from_val(enums.PlutoniumGameModes, self.options[event.value][0]))


    def on_mount(self):
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
        self.my_select.styles.height = "auto"



class PlutoniumGameSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        self.game_mode_label = BasePlutoniumLauncherLabel("Game:")

        # create this from the enum later
        self.options = [
            ("Call of Duty World at War", 0),
            ("Call of Duty Modern Warfare III", 1),
            ("Call of Duty Black Ops I", 2),
            ("Call of Duty Black Ops II", 3),
        ]

        main_value = None
        current_game = get_current_selected_game().value

        for entry in self.options:
            if entry[0] == current_game:
                main_value = entry[1]
                break
            else:
                error_message = 'The currently selected game is invalid.'
                RuntimeWarning(error_message)

        self.my_select: Select[int] = Select(self.options, allow_blank=False, value=main_value)
        with self.horizontal_box:
            yield self.game_mode_label
            yield self.my_select


    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        set_current_selected_game(enums.get_enum_from_val(enums.PlutoniumGames, self.options[event.value][0]))
        from plutonium_launcher_tui.main_app import app
        # below comparison is borked somehow, fix later
        if get_current_selected_game() == enums.PlutoniumGames.CALL_OF_DUTY_MODERN_WARFARE_III.value:
            main_value = 0
        else:
            if get_currently_selected_game_mode() == enums.PlutoniumGameModes.SINGLE_PLAYER:
                main_value = 0
            else:
                main_value = 1
            
        app.plutonium_game_section.game_mode_selector.my_select.value = main_value
        app.plutonium_game_section.game_mode_selector.refresh(recompose=True)
        print_to_log_window(f'Loaded settings for: {get_current_selected_game().value}')


    def on_mount(self):
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
        self.my_select.styles.height = "auto"


class PlutoniumGameSection(Static):
    def compose(self) -> ComposeResult:
        self.vertical_box = Vertical()
        self.game_selector = PlutoniumGameSelector()
        self.game_mode_selector = PlutoniumGameModeSelector()
        with self.vertical_box:
            yield self.game_selector
            yield self.game_mode_selector
            yield PlutoniumGameDirectoryBar()

    def on_mount(self):
        self.vertical_box.styles.height = "auto"


class AddUserButton(Static):
    def compose(self) -> ComposeResult:
        self.add_button = BasePlutoniumLauncherButton(button_text="+", button_width="auto")
        yield self.add_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.add_button.styles.height = "auto"
        self.add_button.styles.text_align = "center"
        self.add_button.styles.align = ("center", "middle")
        self.add_button.styles.content_align = ("center", "middle")

    def on_button_pressed(self) -> None:
        from plutonium_launcher_tui.main_app import app
        app.global_args_screen.refresh(recompose=True)
        app.push_screen(app.username_screen)


class RemoveUserButton(Static):
    def compose(self) -> ComposeResult:
        self.add_button = BasePlutoniumLauncherButton(button_text="-", button_width="auto")
        yield self.add_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.add_button.styles.height = "auto"
        self.add_button.styles.text_align = "center"
        self.add_button.styles.align = ("center", "middle")
        self.add_button.styles.content_align = ("center", "middle")

    def on_button_pressed(self) -> None:
        from plutonium_launcher_tui.main_app import app
        from plutonium_launcher_tui.settings import remove_username

        username = app.user_bar.options[app.user_bar.usernames_combo_box.value][0]

        print_to_log_window(f'Attempting to remove the following username: "{username}"')
        remove_username(username)
        app.user_bar.refresh(recompose=True)


class PlutoniumUserBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox(padding=(1, 0, 0, 0), width="100%")
        self.user_label = BasePlutoniumLauncherLabel(label_text="User:", label_height="auto")
        self.options = []
        for index, username in enumerate(get_usernames()):
            self.options.append((username, index))

        main_value = None
        current_username = get_current_username()

        for entry in self.options:
            if entry[0] == current_username:
                main_value = entry[1]
                break
            else:
                error_message = 'The currently selected game is invalid.'
                RuntimeWarning(error_message)

        self.usernames_combo_box: Select[int] = Select(options=self.options, allow_blank=False, value=main_value)
        self.add_button = AddUserButton()
        self.remove_button = RemoveUserButton()
        with self.horizontal_box:
            yield self.user_label
            yield self.usernames_combo_box
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box

    def on_mount(self):
        self.add_button.styles.height = "100%"
        self.remove_button.styles.height = "100%"


class AppDataButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text="AppData Directory", button_width="100%")
        yield self.button

    def on_button_pressed(self) -> None:
        plutonium_appdata_folder = os.path.normpath(os.path.abspath(f'{os.getenv('APPDATA')}/../Local/Plutonium'))
        open_directory_in_file_browser(plutonium_appdata_folder)

    def on_mount(self):
        self.styles.width = "33%"


class GameDirectoryButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text="Game Directory", button_width="100%")
        yield self.button

    def on_button_pressed(self) -> None:
        game_dir = get_game_directory()
        if os.path.isdir(game_dir):
            open_directory_in_file_browser(game_dir)

    def on_mount(self):
        self.styles.width = "33%"


class RunGameButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text='Run Game', button_width='100%')
        yield self.button

    def on_button_pressed(self) -> None:
        print_to_log_window('Run Game')

    def on_mount(self):
        self.styles.width = "33%"


class PlutoniumGameBar(Static):
    def compose(self) -> ComposeResult:
        with BasePlutoniumLauncherHorizontalBox():
            yield AppDataButton()
            yield GameDirectoryButton()
            yield RunGameButton()


class DocsButton(Static):
    def compose(self) -> ComposeResult:
        self.docs_button = BasePlutoniumLauncherButton(button_text="Docs", button_width="100%")
        yield self.docs_button

    def on_button_pressed(self) -> None:
        url = "https://plutonium.pw/docs/"
        open_website(url)

    def on_mount(self):
        self.styles.width = "33%"


class ForumsButton(Static):
    def compose(self) -> ComposeResult:
        self.forums_button = BasePlutoniumLauncherButton(button_text="Forums", button_width="100%")
        yield self.forums_button

    def on_button_pressed(self) -> None:
        url = "https://forum.plutonium.pw/"
        open_website(url)

    def on_mount(self):
        self.styles.width = "33%"


class GithubButton(Static):
    def compose(self) -> ComposeResult:
        self.github_button = BasePlutoniumLauncherButton(button_text="Github", button_width="100%")
        yield self.github_button

    def on_button_pressed(self) -> None:
        url = "https://github.com/Mythical-Github/plutonium_launcher_tui"
        open_website(url)

    def on_mount(self):
        self.styles.width = "33%"


class PlutoniumWebsiteBar(Static):
    def compose(self) -> ComposeResult:
        with BasePlutoniumLauncherHorizontalBox(padding=(0)):
            yield DocsButton()
            yield GithubButton()
            yield ForumsButton()


class ConfirmUserNameButton(Static):
    def compose(self) -> ComposeResult:
        self.confirm_button = BasePlutoniumLauncherButton(button_text='Confirm')
        yield self.confirm_button

    def on_mount(self):
        self.confirm_button.styles.width = 'auto'
        self.styles.width = 'auto'
        self.styles.height = 'auto'

    def on_button_pressed(self) -> None:
        simulate_confirm_username_button_pressed()


def simulate_cancel_username_button_pressed():
    from plutonium_launcher_tui.main_app import app
    app.username_screen.username_input.text_input.value = ''
    app.pop_screen()


def simulate_confirm_username_button_pressed():
        from plutonium_launcher_tui.main_app import app
        text_value = app.username_screen.username_input.text_input.value

        if not text_value or text_value.strip() == '':
            app.user_bar.refresh(recompose=True)
            print_to_log_window('You cannot add a blank username')
            app.pop_screen()
            return
        elif text_value in get_usernames():
            app.user_bar.refresh(recompose=True)
            print_to_log_window('You cannot add a username that already exists')
            app.pop_screen()
            return
        else:
            set_username(text_value)
            text_value = ''
            app.user_bar.refresh(recompose=True)
            app.pop_screen()
        app.username_screen.username_input.text_input.value = ''


class CancelUserNameButton(Static):
    def compose(self) -> ComposeResult:
        self.cancel_button = BasePlutoniumLauncherButton(button_text='Cancel')
        yield self.cancel_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.cancel_button.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        simulate_cancel_username_button_pressed()


class UsernameActualInput(Input):
    @on(Input.Submitted)
    def on_input_changed(self):
        simulate_confirm_username_button_pressed()


class UsernameInput(Static):
    BINDINGS = [
        ("escape", "cancel_username", "Simulates Hitting the Cancel Button")
    ]
    def compose(self) -> ComposeResult:
        self.label = BasePlutoniumLauncherLabel(
            label_text='Input your new username',
            label_border=('hidden', 'grey'),
            label_padding=(0, 0, 1, 0)
        )
        self.text_input = UsernameActualInput()
        self.vertical_scrollbox = VerticalScroll()
        self.horizontal_bar = BasePlutoniumLauncherHorizontalBox(padding=0)
        self.cancel_button = CancelUserNameButton()
        self.confirm_button = ConfirmUserNameButton()
        with self.vertical_scrollbox:
            yield self.label
            with self.horizontal_bar:
                yield self.text_input
                yield self.cancel_button
                yield self.confirm_button
            yield self.horizontal_bar
        yield self.vertical_scrollbox

    def on_mount(self):
        self.label.styles.width = '100%'
        self.horizontal_bar.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.content_align = ('center', 'middle')
        self.text_input.styles.width = '1fr'
        self.horizontal_bar.styles.border = ('solid', 'grey')
        
        from plutonium_launcher_tui.main_app import app
        app.set_focus(self.text_input)

    def action_cancel_username(self):
        simulate_cancel_username_button_pressed()


class UsernameScreen(Screen):
    def compose(self) -> ComposeResult:
        self.header = Header()
        self.username_input = UsernameInput()
        self.vertical_scroll = VerticalScroll()
        with self.vertical_scroll:
            yield self.header
            yield self.username_input
        yield self.vertical_scroll

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")
        self.vertical_scroll.styles.align = ('center', 'middle')


class GameDirectoryScreen(Screen):
    def compose(self) -> ComposeResult:
        self.header = Header()
        self.vertical_scroll = VerticalScroll()
        with self.vertical_scroll:
            yield self.header
        yield self.vertical_scroll

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")
        self.vertical_scroll.styles.align = ('center', 'middle')


class ConfirmGlobalArgButton(Static):
    def compose(self) -> ComposeResult:
        self.confirm_button = BasePlutoniumLauncherButton(button_text='Confirm')
        yield self.confirm_button

    def on_mount(self):
        self.confirm_button.styles.width = 'auto'
        self.styles.width = 'auto'
        self.styles.height = 'auto'

    def on_button_pressed(self) -> None:
        simulate_confirm_global_arg_button_pressed()


class CancelGlobalArgButton(Static):
    def compose(self) -> ComposeResult:
        self.cancel_button = BasePlutoniumLauncherButton(button_text='Cancel')
        yield self.cancel_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.cancel_button.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        simulate_cancel_global_arg_button_pressed()


def simulate_cancel_global_arg_button_pressed():
    from plutonium_launcher_tui.main_app import app
    app.global_args_screen.global_args_input.text_input.value = ''
    app.pop_screen()


def simulate_confirm_global_arg_button_pressed():
        from plutonium_launcher_tui.main_app import app
        text_value = app.global_args_screen.global_args_input.text_input.value

        if not text_value or text_value.strip() == '':
            app.global_args_section.refresh(recompose=True)
            print_to_log_window('You cannot add a blank argument')
            app.pop_screen()
            return
        elif text_value in get_global_args():
            app.global_args_section.refresh(recompose=True)
            text_value = ''
            print_to_log_window('You cannot add a global argument that already exists')
            app.pop_screen()
            return
        else:
            add_global_arg(text_value)
            text_value = ''
            app.global_args_section.refresh(recompose=True)
            app.pop_screen()
        app.global_args_screen.global_args_input.text_input.value = ''


class GlobalArgsActualInput(Input):
    @on(Input.Submitted)
    def on_input_changed(self):
        simulate_confirm_global_arg_button_pressed()



class GlobalArgsInput(Static):
    BINDINGS = [
            ("escape", "cancel_global_arg", "Simulates Hitting the Cancel Button")
        ]
    def compose(self) -> ComposeResult:
        self.label = BasePlutoniumLauncherLabel(
            label_text='Input the new global argument',
            label_border=('hidden', 'grey'),
            label_padding=(0, 0, 1, 0)
        )
        self.text_input = GlobalArgsActualInput()
        self.vertical_scrollbox = VerticalScroll()
        self.horizontal_bar = BasePlutoniumLauncherHorizontalBox(padding=0)
        self.cancel_button = CancelGlobalArgButton()
        self.confirm_button = ConfirmGlobalArgButton()
        with self.vertical_scrollbox:
            yield self.label
            with self.horizontal_bar:
                yield self.text_input
                yield self.cancel_button
                yield self.confirm_button
            yield self.horizontal_bar
        yield self.vertical_scrollbox

    def on_mount(self):
        self.label.styles.width = '100%'
        self.horizontal_bar.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.content_align = ('center', 'middle')
        self.text_input.styles.width = '1fr'
        self.horizontal_bar.styles.border = ('solid', 'grey')
        
        from plutonium_launcher_tui.main_app import app
        app.set_focus(self.text_input)

    def action_cancel_global_arg(self):
        simulate_cancel_global_arg_button_pressed()


class GlobalArgsScreen(Screen):
    def compose(self) -> ComposeResult:
        self.header = Header()
        self.vertical_scroll = VerticalScroll()
        self.global_args_input = GlobalArgsInput()
        with self.vertical_scroll:
            yield self.header
            yield self.global_args_input
        yield self.vertical_scroll

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")
        self.vertical_scroll.styles.align = ('center', 'middle')


class ConfirmGameArgButton(Static):
    def compose(self) -> ComposeResult:
        self.confirm_button = BasePlutoniumLauncherButton(button_text='Confirm')
        yield self.confirm_button

    def on_mount(self):
        self.confirm_button.styles.width = 'auto'
        self.styles.width = 'auto'
        self.styles.height = 'auto'

    def on_button_pressed(self) -> None:
        simulate_confirm_game_arg_button_pressed()


class CancelGameArgButton(Static):
    def compose(self) -> ComposeResult:
        self.cancel_button = BasePlutoniumLauncherButton(button_text='Cancel')
        yield self.cancel_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.cancel_button.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        from plutonium_launcher_tui.main_app import app
        self.parent.parent.parent.text_input.value = ''
        app.pop_screen()


def simulate_cancel_game_arg_button_pressed():
    from plutonium_launcher_tui.main_app import app
    app.game_args_screen.game_args_input.text_input.value = ''
    app.pop_screen()


def simulate_confirm_game_arg_button_pressed():
    from plutonium_launcher_tui.main_app import app
    text_value = app.game_args_screen.game_args_input.text_input.value

    if not text_value or text_value.strip() == '':
        print_to_log_window('You cannot add a blank argument')
    elif text_value in get_game_specific_args():
        print_to_log_window('You cannot add a game argument that already exists')
    else:
        add_game_specific_arg(text_value)

    app.game_args_section.refresh(recompose=True)
    app.pop_screen()
    text_value = ''


class GameArgsActualInput(Input):
    @on(Input.Submitted)
    def on_input_changed(self):
        simulate_confirm_game_arg_button_pressed()


class GameArgsInput(Static):
    BINDINGS = [
            ("escape", "cancel_game_arg", "Simulates Hitting the Cancel Button")
        ]
    def compose(self) -> ComposeResult:
        self.label = BasePlutoniumLauncherLabel(
            label_text='Input the new game argument',
            label_border=('hidden', 'grey'),
            label_padding=(0, 0, 1, 0)
        )
        self.text_input = GameArgsActualInput()
        self.vertical_scrollbox = VerticalScroll()
        self.horizontal_bar = BasePlutoniumLauncherHorizontalBox(padding=0)
        self.cancel_button = CancelGameArgButton()
        self.confirm_button = ConfirmGameArgButton()
        with self.vertical_scrollbox:
            yield self.label
            with self.horizontal_bar:
                yield self.text_input
                yield self.cancel_button
                yield self.confirm_button
            yield self.horizontal_bar
        yield self.vertical_scrollbox

    def on_mount(self):
        self.label.styles.width = '100%'
        self.horizontal_bar.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.content_align = ('center', 'middle')
        self.text_input.styles.width = '1fr'
        self.horizontal_bar.styles.border = ('solid', 'grey')
        
        from plutonium_launcher_tui.main_app import app
        app.set_focus(self.text_input)

    def action_cancel_game_arg(self):
        simulate_cancel_game_arg_button_pressed()


class GameArgsScreen(Screen):
    def compose(self) -> ComposeResult:
        self.header = Header()
        self.vertical_scroll = VerticalScroll()
        self.game_args_input = GameArgsInput()
        with self.vertical_scroll:
            yield self.header
            yield self.game_args_input
        yield self.vertical_scroll

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")
        self.vertical_scroll.styles.align = ('center', 'middle')
