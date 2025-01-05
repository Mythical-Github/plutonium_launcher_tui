import os

from textual import on
from textual.app import ComposeResult
from textual.widgets import Checkbox, Select, Static
from textual_spinbox import SpinBox

from plutonium_launcher_tui import enums, game_runner
from plutonium_launcher_tui.base_widgets import (
    BasePlutoniumLauncherButton,
    BasePlutoniumLauncherHorizontalBox,
    BasePlutoniumLauncherLabel,
)
from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.os_file_browser import open_directory_in_file_browser
from plutonium_launcher_tui.os_web_browser import open_website
from plutonium_launcher_tui.settings import (
    get_auto_run_game,
    get_auto_run_game_delay,
    get_current_selected_game,
    get_current_username,
    get_currently_selected_game_mode,
    get_game_directory,
    get_game_mode_options,
    get_game_specific_args,
    get_global_args,
    get_use_staging,
    get_usernames,
    set_auto_run_game,
    set_current_selected_game,
    set_currently_selected_game_mode,
    set_use_staging,
)


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
    return len(get_game_specific_args()) == 0


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

delay_spinbox = None
def get_spinbox():
    global delay_spinbox
    return delay_spinbox


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
        global delay_spinbox
        delay_spinbox = self.auto_execute_delay_spin_box


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
            self.game_dir_location_label = BasePlutoniumLauncherLabel(
                get_game_directory(),
                label_width='1fr',
                label_content_align=('left', 'top'),
                label_height='auto'
            )
            self.select_dir_button = SelectGameDirectoryButton()
            yield self.game_dir_label
            yield self.game_dir_location_label
            yield self.select_dir_button

    def on_mount(self):
        self.styles.width = '100%'
        self.styles.height = 'auto'
        self.styles.padding = 0
        self.styles.margin = 0
        self.select_dir_button.styles.text_align = "center"
        self.select_dir_button.styles.align = ("center", "middle")
        self.select_dir_button.styles.content_align = ("center", "middle")
        self.select_dir_button.styles.height = "auto"


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
        if get_current_selected_game() == enums.PlutoniumGames.CALL_OF_DUTY_MODERN_WARFARE_III.value or get_currently_selected_game_mode() == enums.PlutoniumGameModes.SINGLE_PLAYER:
            main_value = 0
        else:
            main_value = 1

        app.game_mode_selector.my_select.value = main_value
        app.game_mode_selector.refresh(recompose=True)
        app.game_dir_select.refresh(recompose=True)
        app.game_args_section.refresh(recompose=True)
        print_to_log_window(f'Loaded settings for: {get_current_selected_game().value}')


    def on_mount(self):
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
        self.my_select.styles.height = "auto"


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
        game_runner.run_game()

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
