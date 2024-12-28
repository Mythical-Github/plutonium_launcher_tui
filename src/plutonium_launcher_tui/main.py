import sys

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import TextArea, Static, Checkbox, Select, Header
from textual_spinbox import SpinBox

from plutonium_launcher_tui.base_widgets import *


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
                label_content_align=('left', 'middle')
            )
            self.auto_execute_checkbox = Checkbox()
            self.auto_execute_delay_label = BasePlutoniumLauncherLabel(
                'Delay in Seconds:',
                label_content_align=('left', 'middle')
            )
            self.auto_execute_delay_spin_box = SpinBox(iter_val=list(generate_spinbox_numbers()), init_val=1.0)
            yield self.auto_execute_label
            yield self.auto_execute_checkbox
            yield self.auto_execute_delay_label
            yield self.auto_execute_delay_spin_box
    
    
    def on_mount(self):
        self.auto_execute_delay_spin_box.styles.width = '22%'
        self.auto_execute_checkbox.styles.width = '14%'
        self.auto_execute_label.styles.width = '28%'
        self.auto_execute_delay_label.styles.width = '36%'
        self.auto_execute_checkbox.styles.content_align = ('center', 'middle')


class PlutoniumGameDirectoryBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        with self.horizontal_box:
            self.game_dir_label = BasePlutoniumLauncherLabel('Game Directory:')
            self.game_dir_text_area = TextArea('path/to/your/game/dir')
            self.select_dir_button = BasePlutoniumLauncherButton(
                button_text='..', 
                button_width=6, 
                button_border=('none', 'black')
            )
            yield self.game_dir_label
            yield self.game_dir_text_area
            yield self.select_dir_button


    def on_mount(self):
        self.game_dir_text_area.styles.height = 'auto'
        self.select_dir_button.styles.text_align = 'center'
        self.select_dir_button.styles.align = ('center', 'middle')
        self.select_dir_button.styles.content_align = ('center', 'middle')
        self.select_dir_button.styles.height = '100%'


class PlutoniumGameModeSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        self.game_mode_label = BasePlutoniumLauncherLabel('Game Mode:')

        options = [
            ("Single Player", 1), 
            ("Multiplayer", 2)
        ]

        self.my_select: Select[int] = Select(options, allow_blank=False)
        with self.horizontal_box:
            yield self.game_mode_label
            yield(self.my_select)


    def on_mount(self):
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
        self.my_select.styles.height = 'auto'


class PlutoniumGameSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        self.game_mode_label = BasePlutoniumLauncherLabel('Game:')

        options = [
            ("Call of Duty World at War", 1), 
            ("Call of Duty Modern Warfare III", 2), 
            ("Call of Duty Black Ops", 3), 
            ("Call of Duty Black Ops II", 4)
        ] 

        self.my_select: Select[int] = Select(options, allow_blank=False)
        with self.horizontal_box:
            yield self.game_mode_label
            yield(self.my_select)


    def on_mount(self):    
        # self.horizontal_box.styles.padding = (1, 0, 0, 0)
        # self.horizontal_box.styles.border = ('solid', 'grey')
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
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
        # self.user_text_area = TextArea('Default Username')]
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
            # yield self.user_text_area
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box
    

    def on_mount(self):
        # self.user_text_area.styles.height = '100%'
        # self.user_text_area.styles.content_align = ('center', 'middle')
        # self.user_text_area.styles.width = 'auto'
        self.add_button.styles.height = '100%'
        self.remove_button.styles.height = '100%'
        self.add_button.styles.text_align = ('center')
        self.add_button.styles.align = ('center', 'middle')
        self.add_button.styles.content_align = ('center', 'middle')


class PlutoniumGameBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox()
        with self.horizontal_box:
            self.app_data_button = BasePlutoniumLauncherButton(button_text='AppData')
            self.game_dir_button = BasePlutoniumLauncherButton(button_text='Game Directory')
            self.run_game_button = BasePlutoniumLauncherButton(button_text='Run Game')
            yield self.app_data_button
            yield self.game_dir_button
            yield self.run_game_button


class PlutoniumWebsiteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BasePlutoniumLauncherHorizontalBox(padding=(0))
        with self.horizontal_box:
            self.docs_button = BasePlutoniumLauncherButton(button_text='Docs')
            self.github_button = BasePlutoniumLauncherButton(button_text='Github')
            self.forums_button = BasePlutoniumLauncherButton(button_text='Forums')
            yield self.docs_button
            yield self.forums_button
            yield self.github_button


class PlutoniumLauncherLog(Static):
    def compose(self):
        self.rich_log = RichLog()
        yield self.rich_log
        return super().compose()
    
    def mount(self, *widgets, before = None, after = None):
        self.rich_log.styles.height = '6'
        self.rich_log.styles.margin = 1
        self.rich_log.styles.border = ('solid', 'grey')
        self.rich_log.border_title = 'Logging'
        self.rich_log.styles.width = '100%'
        return super().mount(*widgets, before=before, after=after)


class PlutoniumLauncher(App):
    TITLE = 'Plutonium Launcher'
    def compose(self) -> ComposeResult:
        self.main_vertical_scroll_box = VerticalScroll()
        with self.main_vertical_scroll_box:
            yield Header()
            yield PlutoniumGameSection()
            yield PlutoniumUserBar()
            yield PlutoniumGameSpecificArgsSection()
            yield PlutoniumGlobalArgsSection()
            yield PlutoniumGameAutoExecuteBar()
            yield PlutoniumGameBar()
            yield PlutoniumWebsiteBar()
            yield PlutoniumLauncherLog()

    def on_mount(self):
        self.main_vertical_scroll_box.styles.margin = (0)
        self.main_vertical_scroll_box.styles.padding = (0)
        self.main_vertical_scroll_box.styles.border = ('solid', 'grey')


app = PlutoniumLauncher()

# sets window title
sys.stdout.write(f'\033]0;{app.TITLE}\007')
sys.stdout.flush()

app.run()
