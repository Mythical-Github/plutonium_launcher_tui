import os
import webbrowser

from textual_spinbox import SpinBox
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import (
    TextArea, 
    Static, 
    Checkbox, 
    Select,
    Button
)

from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.settings import SETTINGS, save_settings
from plutonium_launcher_tui.base_widgets import (
    BasePlutoniumLauncherButton, 
    BasePlutoniumLauncherHorizontalBox, 
    BasePlutoniumLauncherLabel
)


def open_directory_in_file_browser(directory_path: str):
    if os.path.isdir(directory_path):
        os.startfile(directory_path)
        print_to_log_window(f'Opening the following directory in the file browser: "{directory_path}"')
    else:
        print_to_log_window(f'The specified path is not a directory: "{directory_path}"')


def open_website(url: str):
    try:
        webbrowser.open(url, new=2)
        return True
    except Exception as e:
        print(f'An error occurred: {e}')
        return False


class PlutoniumGlobalArgsSection(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()

        options = [
            ('example_one', 1),
            ('example_two', 2)
        ]

        self.combo_box: Select[int] = Select(options, allow_blank=False)

        self.game_args_label = BasePlutoniumLauncherLabel(
            label_text='Global Args:', 
            label_height='auto'
        )

        self.add_button = BasePlutoniumLauncherButton(
            button_text='+', 
            button_width='auto'
        )

        self.remove_button = BasePlutoniumLauncherButton(
            button_text='-', 
            button_width='auto'
        )

        with self.horizontal_box:
            yield self.game_args_label
            yield self.combo_box
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box


    def on_mount(self):
        self.game_args_label.styles.height = 'auto'


class PlutoniumGameSpecificArgsSection(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()

        options = [
            ('example_one', 1),
            ('example_two', 2)
        ]

        self.combo_box: Select[int] = Select(options, allow_blank=False)

        self.game_args_label = BasePlutoniumLauncherLabel(
            label_text='Game Args:', 
            label_height='auto'
        )

        self.add_button = BasePlutoniumLauncherButton(
            button_text='+', 
            button_width='auto'
        )

        self.remove_button = BasePlutoniumLauncherButton(
            button_text='-', 
            button_width='auto'
        )

        with self.horizontal_box:
            yield self.game_args_label
            yield self.combo_box
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box


    def on_mount(self):
        self.game_args_label.styles.height = 'auto'


def generate_spinbox_numbers():
    current = 0
    while current <= 1000:
        yield round(current, 1)
        current += 0.1


class PlutoniumGameAutoExecuteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox(width='100%')
        with self.horizontal_box:
            self.auto_execute_label = BasePlutoniumLauncherLabel(
                'Auto Run Game:',
                label_content_align=('center', 'middle')
            )
            self.auto_execute_checkbox = Checkbox()
            self.auto_execute_delay_label = BasePlutoniumLauncherLabel(
                'Delay in Seconds:',
                label_content_align=('center', 'middle')
            )
            self.auto_execute_delay_spin_box = SpinBox(iter_val=list(generate_spinbox_numbers()), init_val=1.0)
            yield self.auto_execute_label
            yield self.auto_execute_checkbox
            yield self.auto_execute_delay_label
            yield self.auto_execute_delay_spin_box
    
    
    def on_mount(self):
        self.auto_execute_delay_spin_box.styles.width = '33%'
        self.auto_execute_checkbox.styles.width = '10%'
        self.auto_execute_label.styles.width = '26%'
        self.auto_execute_delay_label.styles.width = '31%'
        self.auto_execute_checkbox.styles.content_align = ('center', 'middle')


class PlutoniumGameDirectoryBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        with self.horizontal_box:
            self.game_dir_label = BasePlutoniumLauncherLabel('Game Directory:')
            self.game_dir_text_area = TextArea('path/to/your/game/dir')
            self.select_dir_button = BasePlutoniumLauncherButton(
                button_text='··', 
                button_width=6, 
                button_border=('none', 'black')
            )
            yield self.game_dir_label
            yield self.game_dir_text_area
            yield self.select_dir_button


    def on_mount(self):
        self.game_dir_text_area.styles.height = '3'
        self.select_dir_button.styles.text_align = 'center'
        self.select_dir_button.styles.align = ('center', 'middle')
        self.select_dir_button.styles.content_align = ('center', 'middle')
        self.select_dir_button.styles.height = 'auto'


class PlutoniumGameModeSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        self.game_mode_label = BasePlutoniumLauncherLabel('Game Mode:')

        options = [
            ('Single Player', 1), 
            ('Multiplayer', 2)
        ]

        self.my_select: Select[int] = Select(options, allow_blank=False)
        with self.horizontal_box:
            yield self.game_mode_label
            yield(self.my_select)


    def on_mount(self):
        self.my_select.styles.content_align = ('center', 'middle')
        self.my_select.styles.align = ('center', 'middle')
        self.my_select.styles.height = 'auto'


class PlutoniumGameSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        self.game_mode_label = BasePlutoniumLauncherLabel('Game:')

        options = [
            ('Call of Duty World at War', 1), 
            ('Call of Duty Modern Warfare III', 2), 
            ('Call of Duty Black Ops', 3), 
            ('Call of Duty Black Ops II', 4)
        ] 

        self.my_select: Select[int] = Select(options, allow_blank=False)
        with self.horizontal_box:
            yield self.game_mode_label
            yield(self.my_select)


    def on_mount(self):
        self.my_select.styles.content_align = ('center', 'middle')
        self.my_select.styles.align = ('center', 'middle')
        self.my_select.styles.height = 'auto'


class PlutoniumGameSection(Static):
    def compose(self) -> ComposeResult:
        self.vertical_box = Vertical()
        with self.vertical_box:
            yield PlutoniumGameSelector()
            yield PlutoniumGameModeSelector()
            yield PlutoniumGameDirectoryBar()
    

    def on_mount(self):
        self.vertical_box.styles.height = 'auto'


class PlutoniumUserBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox(padding=(1, 0, 0, 0), width='100%')
        self.user_label = BasePlutoniumLauncherLabel(label_text='User:', label_height='auto')
        options = [
            ('default', 0),
            ('default_two', 1)
        ]
        self.usernames_combo_box: Select[int] = Select(options, allow_blank=False)
        self.add_button = BasePlutoniumLauncherButton(button_text='+', button_width='auto')
        self.remove_button = BasePlutoniumLauncherButton(button_text='-', button_width='auto')
        with self.horizontal_box:
            yield self.user_label
            yield self.usernames_combo_box
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box
    

    def on_mount(self):
        self.add_button.styles.height = '100%'
        self.remove_button.styles.height = '100%'
        self.add_button.styles.text_align = ('center')
        self.add_button.styles.align = ('center', 'middle')
        self.add_button.styles.content_align = ('center', 'middle')


class AppDataButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text='AppData', button_width='100%')
        yield self.button
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        plutonium_appdata_folder = os.path.normpath(os.path.abspath(f'{os.getenv('APPDATA')}/../Local/Plutonium'))
        open_directory_in_file_browser(plutonium_appdata_folder)

    def mount(self, *widgets, before = None, after = None):
        self.styles.width = '33%'
        return super().mount(*widgets, before=before, after=after)


class GameDirectoryButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text='Game Directory', button_width='100%')
        yield self.button
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        print_to_log_window(f'Game Directory')

    def mount(self, *widgets, before = None, after = None):
        self.styles.width = '33%'
        return super().mount(*widgets, before=before, after=after)


class RunGameButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BasePlutoniumLauncherButton(button_text='Run Game', button_width='100%')
        yield self.button
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        print_to_log_window(SETTINGS['global']['auto_run_game'])
        print_to_log_window(f'Run Game')

    def mount(self, *widgets, before = None, after = None):
        self.styles.width = '33%'
        return super().mount(*widgets, before=before, after=after)


class PlutoniumGameBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        with self.horizontal_box:
            self.app_data_button = AppDataButton()
            self.game_dir_button = GameDirectoryButton()
            self.run_game_button = RunGameButton()
            yield self.app_data_button
            yield self.game_dir_button
            yield self.run_game_button


class DocsButton(Static):
    def compose(self) -> ComposeResult:
        self.docs_button = BasePlutoniumLauncherButton(button_text='Docs', button_width='100%')
        yield self.docs_button
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        url = 'https://plutonium.pw/docs/'
        print_to_log_window(f'Opening website url: {url}')
        open_website(url)

    def mount(self, *widgets, before = None, after = None):
        self.styles.width = '33%'
        return super().mount(*widgets, before=before, after=after)


class ForumsButton(Static):
    def compose(self) -> ComposeResult:
        self.forums_button = BasePlutoniumLauncherButton(button_text='Forums', button_width='100%')
        yield self.forums_button
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        url = 'https://forum.plutonium.pw/'
        print_to_log_window(f'Opening website url: {url}')
        open_website(url)

    def mount(self, *widgets, before = None, after = None):
        self.styles.width = '33%'
        return super().mount(*widgets, before=before, after=after)


class GithubButton(Static):
    def compose(self) -> ComposeResult:
        self.github_button = BasePlutoniumLauncherButton(button_text='Github', button_width='100%')
        yield self.github_button
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        url = 'https://github.com/Mythical-Github/plutonium_launcher_tui'
        print_to_log_window(f'Opening website url: {url}')
        open_website(url)

    def mount(self, *widgets, before = None, after = None):
        self.styles.width='33%'
        return super().mount(*widgets, before=before, after=after)


class PlutoniumWebsiteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox(padding=(0))
        self.docs_button = DocsButton()
        self.github_button = GithubButton()
        self.forums_button = ForumsButton()
        with self.horizontal_box:
            yield self.docs_button
            yield self.forums_button
            yield self.github_button
        yield self.horizontal_box