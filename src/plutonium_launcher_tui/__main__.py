from textual.widgets import TextArea, Button, Label, Static, Checkbox, Select, Header
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.app import App, ComposeResult


class PlutoniumGameSpecificArgButtonList(Static):
    def compose(self) -> ComposeResult:
        self.vertical_box = Vertical()
        self.text_area = TextArea('default_arg_text')
        with self.vertical_box:
            yield self.text_area
            yield Button('Add')
            yield Button('Remove')


    def on_mount(self):
        self.vertical_box.styles.width = 'auto'
        self.text_area.styles.height = 'auto'


class PlutoniumGameSpecificArgsSection(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        with self.horizontal_box:
            yield Label('test')
            yield PlutoniumGameSpecificArgButtonList()


class PlutoniumGameAutoExecuteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        with self.horizontal_box:
            self.auto_execute_label = Label('Auto Execute:')
            self.auto_execute_checkbox = Checkbox()
            self.auto_execute_delay_label = Label('Delay in Seconds:')
            self.auto_execute_delay_text_area = TextArea('1.0')
            yield self.auto_execute_label
            yield self.auto_execute_checkbox
            yield self.auto_execute_delay_label
            yield self.auto_execute_delay_text_area
    
    
    def on_mount(self):
        self.horizontal_box.styles.margin = (1)
        self.horizontal_box.styles.height = 'auto'
        self.auto_execute_delay_text_area.styles.height = 'auto'
        self.auto_execute_delay_label.styles.content_align = ("center", "middle")
        self.auto_execute_label.styles.height = '100%'
        self.auto_execute_label.styles.content_align = ("center", "middle")
        self.auto_execute_delay_label.styles.height = '100%'
        self.auto_execute_delay_label.styles.border = ("solid", "black")
        self.auto_execute_label.styles.border = ("solid", "black")


class PlutoniumGameDirectoryBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        with self.horizontal_box:
            self.game_dir_label = Label('Game Directory:')
            self.game_dir_text_area = TextArea('path/to/your/game/dir')
            yield self.game_dir_label
            yield self.game_dir_text_area


    def on_mount(self):
        self.horizontal_box.styles.margin = (1)
        self.horizontal_box.styles.height = 'auto'
        self.game_dir_text_area.styles.height = 'auto'
        self.game_dir_label.styles.height = '100%'
        self.game_dir_label.styles.content_align = ("center", "middle")
        self.game_dir_label.styles.border = ("solid", "black")


class PlutoniumGameModeSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        self.game_mode_label = Label('Game Mode:')
        options = [("Single Player", 1), ("Multiplayer", 2)]
        self.my_select: Select[int] = Select(options)
        with self.horizontal_box:
            yield self.game_mode_label
            yield(self.my_select)


    def on_mount(self):    
        self.horizontal_box.styles.margin = (1)
        self.horizontal_box.styles.height = 'auto'
        for child in self.horizontal_box.children:
            if isinstance(child, Label):
                child.styles.content_align = ("center", "middle")
                child.styles.height = '100%'
                child.styles.border = ("solid", "black")


class PlutoniumGameSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        self.game_mode_label = Label('Game:')
        options = [("Call of Duty World at War", 1), ("Call of Duty Modern Warfare III", 2), ("Call of Duty Black Ops", 3), ("Call of Duty Black Ops II", 4)] 
        self.my_select: Select[int] = Select(options)
        with self.horizontal_box:
            yield self.game_mode_label
            yield(self.my_select)


    def on_mount(self):    
        self.horizontal_box.styles.margin = (1)
        self.horizontal_box.styles.height = 'auto'
        self.game_mode_label.styles.border = ("solid", "black")
        self.game_mode_label.styles.content_align = ("center", "middle")
        self.game_mode_label.styles.height = '100%'
        self.game_mode_label.styles.border = ("solid", "black")


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
        self.horizontal_box.styles.margin = (1)
        self.horizontal_box.styles.height = 'auto'
        self.user_text_area.styles.height = 'auto'
        self.user_label.styles.content_align = ("center", "middle")
        self.user_label.styles.height = '100%'
        self.user_label.styles.border = ("solid", "black")


class PlutoniumWebsiteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = Horizontal()
        with self.horizontal_box:
            self.docs_button = Button('Docs')
            self.github_button = Button('Github')
            self.forums_button = Button('Forums')
            yield self.docs_button
            yield self.forums_button
            yield self.github_button
        
    
    def on_mount(self):
        self.horizontal_box.styles.height = 'auto'
        self.github_button.styles.width = '33%'
        self.forums_button.styles.width = '33%'
        self.docs_button.styles.width = '33%'
        self.horizontal_box.styles.margin = (1)
        self.forums_button.styles.margin = (1)
        self.github_button.styles.margin = (1)
        self.docs_button.styles.margin = (1)


class PlutoniumLauncher(App):
    TITLE = 'Plutonium Launcher'
    def compose(self) -> ComposeResult:
        main_vertical_box = VerticalScroll()
        main_vertical_box.styles.margin = (1)
        with main_vertical_box:
            yield Header()
            yield PlutoniumGameSection()
            yield PlutoniumUserBar()
#             yield PlutoniumGameSpecificArgsSection()
            yield PlutoniumWebsiteBar()


if __name__ == "__main__":
    app = PlutoniumLauncher()
    app.run()
