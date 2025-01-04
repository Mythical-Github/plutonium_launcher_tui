from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Header


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
