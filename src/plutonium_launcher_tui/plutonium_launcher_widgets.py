import os
import subprocess
import webbrowser

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Checkbox, Select, Static, TextArea
from textual_spinbox import SpinBox

from plutonium_launcher_tui import enums
from plutonium_launcher_tui.base_widgets import (
    BasePlutoniumLauncherButton,
    BasePlutoniumLauncherHorizontalBox,
    BasePlutoniumLauncherLabel,
)
from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.settings import (
    SETTINGS, 
    get_current_selected_game, 
    get_auto_run_game, 
    get_auto_run_game_delay, 
    get_usernames, 
    get_current_username,
    set_current_selected_game,
    get_currently_selected_game_mode,
    set_currently_selected_game_mode
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


class PlutoniumGlobalArgsSection(Static):
    def compose(self) -> ComposeResult:

        options = [("example_one", 1), ("example_two", 2)]

        self.combo_box: Select[int] = Select(options, allow_blank=False)

        self.add_button = BasePlutoniumLauncherButton(button_text="+", button_width="auto")

        self.remove_button = BasePlutoniumLauncherButton(button_text="-", button_width="auto")

        with BasePlutoniumLauncherHorizontalBox():
            yield BasePlutoniumLauncherLabel(label_text="Global Args:", label_height="auto")
            yield self.combo_box
            yield self.remove_button
            yield self.add_button


class PlutoniumGameSpecificArgsSection(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()

        options = [("example_one", 1), ("example_two", 2)]

        self.combo_box: Select[int] = Select(options, allow_blank=False)

        self.game_args_label = BasePlutoniumLauncherLabel(label_text="Game Args:", label_height="auto")

        self.add_button = BasePlutoniumLauncherButton(button_text="+", button_width="auto")

        self.remove_button = BasePlutoniumLauncherButton(button_text="-", button_width="auto")

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


class PlutoniumGameAutoExecuteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox(width="100%")
        with self.horizontal_box:
            self.auto_execute_label = BasePlutoniumLauncherLabel(
                "Auto Run Game:", 
                label_content_align=("center", "middle"),
                label_width="26%"
            )
            self.auto_execute_checkbox = Checkbox(value=get_auto_run_game())
            self.auto_execute_delay_label = BasePlutoniumLauncherLabel(
                "Delay in Seconds:", 
                label_content_align=("center", "middle"),
                label_width="31%"
            )
            self.auto_execute_delay_spin_box = SpinBox(iter_val=list(generate_spinbox_numbers()), init_val=get_auto_run_game_delay())
            yield self.auto_execute_label
            yield self.auto_execute_checkbox
            yield self.auto_execute_delay_label
            yield self.auto_execute_delay_spin_box

    def on_mount(self):
        self.auto_execute_delay_spin_box.styles.width = "33%"
        self.auto_execute_checkbox.styles.width = "10%"
        self.auto_execute_checkbox.styles.content_align = ("center", "middle")


class PlutoniumGameDirectoryBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        with self.horizontal_box:
            self.game_dir_label = BasePlutoniumLauncherLabel("Game Directory:")
            self.game_dir_text_area = TextArea("path/to/your/game/dir")
            self.select_dir_button = BasePlutoniumLauncherButton(
                button_text="··", button_width=6, button_border=("none", "black")
            )
            yield self.game_dir_label
            yield self.game_dir_text_area
            yield self.select_dir_button

    def on_mount(self):
        self.game_dir_text_area.styles.height = "3"
        self.select_dir_button.styles.text_align = "center"
        self.select_dir_button.styles.align = ("center", "middle")
        self.select_dir_button.styles.content_align = ("center", "middle")
        self.select_dir_button.styles.height = "auto"


class PlutoniumGameModeSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        self.game_mode_label = BasePlutoniumLauncherLabel("Game Mode:")

        # generate this from the enum later
        self.options = [
            ("Single Player", 0), 
            ("Multiplayer", 1)
        ]

        main_value = None
        current_game = get_currently_selected_game_mode().value

        for entry in self.options:
            if entry[0] == current_game:
                main_value = entry[1]
                break
            else:
                error_message = f'The currently selected game is invalid.'
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
                error_message = f'The currently selected game is invalid.'
                RuntimeWarning(error_message)

        self.my_select: Select[int] = Select(self.options, allow_blank=False, value=main_value)
        with self.horizontal_box:
            yield self.game_mode_label
            yield self.my_select


    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        set_current_selected_game(enums.get_enum_from_val(enums.PlutoniumGames, self.options[event.value][0]))
        from plutonium_launcher_tui.main_app import app
        # below comparison is borked somehow
        if get_currently_selected_game_mode() == enums.PlutoniumGameModes.SINGLE_PLAYER:
            main_value = 0
        else:
            main_value = 1
        app.plutonium_game_section.game_mode_selector.my_select.value = main_value
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


class PlutoniumUserBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox(padding=(1, 0, 0, 0), width="100%")
        self.user_label = BasePlutoniumLauncherLabel(label_text="User:", label_height="auto")
        options = []
        for index, username in enumerate(get_usernames()):
            options.append((username, index))
        
        main_value = None
        current_username = get_current_username()

        for entry in options:
            if entry[0] == current_username:
                main_value = entry[1]
                break
            else:
                error_message = f'The currently selected game is invalid.'
                RuntimeWarning(error_message)


        self.usernames_combo_box: Select[int] = Select(options=options, allow_blank=False, value=main_value)
        self.add_button = BasePlutoniumLauncherButton(button_text="+", button_width="auto")
        self.remove_button = BasePlutoniumLauncherButton(button_text="-", button_width="auto")
        with self.horizontal_box:
            yield self.user_label
            yield self.usernames_combo_box
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box

    def on_mount(self):
        self.add_button.styles.height = "100%"
        self.remove_button.styles.height = "100%"
        self.add_button.styles.text_align = "center"
        self.add_button.styles.align = ("center", "middle")
        self.add_button.styles.content_align = ("center", "middle")


class AppDataButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text="AppData", button_width="100%")
        yield self.button

    def on_button_pressed(self) -> None:
        plutonium_appdata_folder = os.path.normpath(os.path.abspath(f'{os.getenv('APPDATA')}/../Local/Plutonium'))
        open_directory_in_file_browser(plutonium_appdata_folder)

    def mount(self, *widgets, before=None, after=None):
        self.styles.width = "33%"
        return super().mount(*widgets, before=before, after=after)


class GameDirectoryButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text="Game Directory", button_width="100%")
        yield self.button

    def on_button_pressed(self) -> None:
        print_to_log_window("Game Directory")

    def mount(self, *widgets, before=None, after=None):
        self.styles.width = "33%"
        return super().mount(*widgets, before=before, after=after)


class RunGameButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text='Run Game', button_width='100%')
        yield self.button

    def on_button_pressed(self) -> None:
        print_to_log_window(SETTINGS['global']['auto_run_game'])
        print_to_log_window('Run Game')

    def mount(self, *widgets, before=None, after=None):
        self.styles.width = "33%"
        return super().mount(*widgets, before=before, after=after)


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

    def mount(self, *widgets, before=None, after=None):
        self.styles.width = "33%"
        return super().mount(*widgets, before=before, after=after)


class ForumsButton(Static):
    def compose(self) -> ComposeResult:
        self.forums_button = BasePlutoniumLauncherButton(button_text="Forums", button_width="100%")
        yield self.forums_button

    def on_button_pressed(self) -> None:
        url = "https://forum.plutonium.pw/"
        open_website(url)

    def mount(self, *widgets, before=None, after=None):
        self.styles.width = "33%"
        return super().mount(*widgets, before=before, after=after)


class GithubButton(Static):
    def compose(self) -> ComposeResult:
        self.github_button = BasePlutoniumLauncherButton(button_text="Github", button_width="100%")
        yield self.github_button

    def on_button_pressed(self) -> None:
        url = "https://github.com/Mythical-Github/plutonium_launcher_tui"
        open_website(url)

    def mount(self, *widgets, before=None, after=None):
        self.styles.width = "33%"
        return super().mount(*widgets, before=before, after=after)


class PlutoniumWebsiteBar(Static):
    def compose(self) -> ComposeResult:
        with BasePlutoniumLauncherHorizontalBox(padding=(0)):
            yield DocsButton()
            yield GithubButton()
            yield ForumsButton()
