from textual.app import *
from textual.widgets import *
from textual.containers import *


class BasePlutoniumLauncherButton(Button):
    def __init__(
            self, 
            button_text: str = 'default_text',
            button_width: str = '33%',
            button_margin: int = 0,
            button_min_width: int = 0,
            button_min_height: int = 0,
            button_border: str = 'none',
            button_padding: int = 0
        ):
        super().__init__()
        self.label = button_text
        self.button_width = button_width
        self.button_margin = button_margin
        self.button_min_width = button_min_width
        self.button_min_height = button_min_height
        self.button_border = button_border
        self.button_padding = button_padding

    def on_mount(self):
        self.styles.width = self.button_width
        self.styles.margin = self.button_margin
        self.styles.min_width = self.button_min_width
        self.styles.border = self.button_border
        self.styles.padding = self.button_padding
        self.styles.min_height = self.button_min_height
        self.styles.border = ('solid', 'grey')
