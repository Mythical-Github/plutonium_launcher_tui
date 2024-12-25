import sys

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import TextArea, Label, Static, Checkbox, Select, Header
from textual_spinbox import SpinBox

from plutonium_launcher_tui.base_widgets import BasePlutoniumLauncherButton


class PlutoniumGameSpecificArgButtonList(Static):
    def compose(self) -> ComposeResult:
        self.vertical_box = Vertical()
        self.add_button = BasePlutoniumLauncherButton(button_text='Add')
        self.remove_button = BasePlutoniumLauncherButton(button_text='Remove')
        with self.vertical_box:
            yield self.add_button
            yield self.remove_button


class PlutoniumGameSpecificArgsSection(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        self.text_area = TextArea('default_arg_text')
        self.game_args_label = Label('Game Args:')
        with self.horizontal_box:
            yield self.game_args_label
            yield self.text_area
            yield PlutoniumGameSpecificArgButtonList()


    def on_mount(self):
        self.horizontal_box.styles.margin = 0
        self.horizontal_box.styles.padding = 0
        self.text_area.styles.height = 'auto'
        self.text_area.styles.width = '24'
        self.text_area.styles.content_align_horizontal = 'center'
        self.text_area.styles.align_horizontal = 'center'
        self.text_area.styles.text_align = 'center'
        self.text_area.styles.content_align = ('center', 'middle')


def generate_spinbox_numbers():
    current = 0
    while current <= 1000:
        yield round(current, 1)
        current += 0.1


class PlutoniumGameAutoExecuteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        with self.horizontal_box:
            self.auto_execute_label = Label('Auto Execute:')
            self.auto_execute_checkbox = Checkbox()
            self.auto_execute_delay_label = Label('Delay in Seconds:')
            self.auto_execute_delay_spin_box = SpinBox(iter_val=list(generate_spinbox_numbers()), init_val=1.0)
            yield self.auto_execute_label
            yield self.auto_execute_checkbox
            yield self.auto_execute_delay_label
            yield self.auto_execute_delay_spin_box
    
    
    def on_mount(self):
        self.horizontal_box.styles.margin = (0)
        self.horizontal_box.styles.padding = (0)
        self.horizontal_box.styles.height = 'auto'
        self.auto_execute_delay_label.styles.content_align = ("center", "middle")
        self.auto_execute_label.styles.height = '100%'
        self.auto_execute_label.styles.width = '28%'
        self.auto_execute_delay_label.width = '28%'
        self.auto_execute_label.styles.content_align = ("center", "middle")
        self.auto_execute_delay_label.styles.height = '100%'
        self.auto_execute_delay_label.styles.border = ('solid', 'grey')
        self.auto_execute_label.styles.border = ('solid', 'grey')
        self.auto_execute_delay_spin_box.styles.width = '24%'
        self.horizontal_box.styles.border = ('solid', 'grey')


class PlutoniumGameDirectoryBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        with self.horizontal_box:
            self.game_dir_label = Label('Game Directory:')
            self.game_dir_text_area = TextArea('path/to/your/game/dir')
            yield self.game_dir_label
            yield self.game_dir_text_area


    def on_mount(self):
        self.horizontal_box.styles.padding = (0)
        self.horizontal_box.styles.margin = (0)
        self.horizontal_box.styles.height = 'auto'
        self.game_dir_text_area.styles.height = 'auto'
        self.game_dir_label.styles.height = '100%'
        self.game_dir_label.styles.content_align = ("center", "middle")
        self.game_dir_label.styles.border = ('solid', 'grey')


class PlutoniumGameModeSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        self.game_mode_label = Label('Game Mode:')

        options = [
            ("Single Player", 1), 
            ("Multiplayer", 2)
        ]

        self.my_select: Select[int] = Select(options, allow_blank=False)
        with self.horizontal_box:
            yield self.game_mode_label
            yield(self.my_select)


    def on_mount(self):    
        self.horizontal_box.styles.margin = (0)
        self.horizontal_box.styles.padding = 0
        self.horizontal_box.styles.height = 'auto'
        # self.horizontal_box.styles.border = ('solid', 'grey')
        self.horizontal_box.styles.content_align = ('center', 'middle')
        self.horizontal_box.styles.align = ('center', 'middle')
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
        self.my_select.styles.height = '100%'
        for child in self.horizontal_box.children:
            if isinstance(child, Label):
                child.styles.content_align = ("center", "middle")
                child.styles.height = 'auto'
                child.styles.border = ('solid', 'grey')
                child.styles.padding = 1


class PlutoniumGameSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        self.game_mode_label = Label('Game:')

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
        self.horizontal_box.styles.margin = (0)
        self.horizontal_box.styles.padding = 0
        self.horizontal_box.styles.height = 'auto'
        # self.horizontal_box.styles.border = ('solid', 'grey')
        self.game_mode_label.styles.border = ('solid', 'grey')
        self.game_mode_label.styles.content_align = ("center", "middle")
        self.game_mode_label.styles.height = 'auto'
        self.game_mode_label.styles.border = ('solid', 'grey')
        self.game_mode_label.styles.padding = 1
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
        self.my_select.styles.height = '100%'


class PlutoniumGameSection(Static):
    def compose(self) -> ComposeResult:
        self.vertical_box = Vertical()
        with self.vertical_box:
            yield PlutoniumGameModeSelector()
            yield PlutoniumGameSelector()
            yield PlutoniumGameAutoExecuteBar()
            yield PlutoniumGameDirectoryBar()
    

    def on_mount(self):
        self.vertical_box.styles.height = 'auto'


class PlutoniumUserBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        self.user_label = Label('User:')
        self.user_text_area = TextArea('Default Username')
        with self.horizontal_box:
            yield self.user_label
            yield self.user_text_area
    

    def on_mount(self):
        self.horizontal_box.styles.margin = (0)
        self.horizontal_box.styles.padding = (0)
        self.horizontal_box.styles.height = 'auto'
        self.user_text_area.styles.height = 'auto'
        self.user_label.styles.content_align = ("center", "middle")
        self.user_label.styles.height = '100%'
        self.user_label.styles.border = ('solid', 'grey')


class PlutoniumWebsiteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        with self.horizontal_box:
            self.docs_button = BasePlutoniumLauncherButton(button_text='Docs')
            self.github_button = BasePlutoniumLauncherButton(button_text='Github')
            self.forums_button = BasePlutoniumLauncherButton(button_text='Forums')
            yield self.docs_button
            yield self.forums_button
            yield self.github_button

    def on_mount(self):
        self.horizontal_box.styles.padding = 0
        self.horizontal_box.styles.margin = 0


class PlutoniumLauncher(App):
    TITLE = 'Plutonium Launcher'
    def compose(self) -> ComposeResult:
        self.main_vertical_scroll_box = Vertical()
        with self.main_vertical_scroll_box:
            yield Header()
            yield PlutoniumGameSection()
            yield PlutoniumUserBar()
            yield PlutoniumGameSpecificArgsSection()
            yield PlutoniumWebsiteBar()

    def on_mount(self):
        self.main_vertical_scroll_box.styles.margin = (0)
        self.main_vertical_scroll_box.styles.padding = (0)
        self.main_vertical_scroll_box.styles.border = ('solid', 'grey')


app = PlutoniumLauncher()

# sets window title
sys.stdout.write(f'\033]0;{app.TITLE}\007')
sys.stdout.flush()

app.run()
