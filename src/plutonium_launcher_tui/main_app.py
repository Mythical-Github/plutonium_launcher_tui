from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header

from plutonium_launcher_tui.customization import set_terminal_size, set_theme, set_window_title
from plutonium_launcher_tui.logger import plutonium_logger
from plutonium_launcher_tui.plutonium_launcher_widgets import (
    PlutoniumGameAutoExecuteBar,
    PlutoniumGameBar,
    PlutoniumGameSection,
    PlutoniumGameSpecificArgsSection,
    PlutoniumGlobalArgsSection,
    PlutoniumUserBar,
    PlutoniumWebsiteBar,
)


class PlutoniumLauncher(App):
    TITLE = "Plutonium Launcher"

    def compose(self) -> ComposeResult:
        self.main_vertical_scroll_box = VerticalScroll()
        self.plutonium_game_section = PlutoniumGameSection()
        with self.main_vertical_scroll_box:
            yield Header()
            yield self.plutonium_game_section
            yield PlutoniumUserBar()
            yield PlutoniumGameSpecificArgsSection()
            yield PlutoniumGlobalArgsSection()
            yield PlutoniumGameAutoExecuteBar()
            yield PlutoniumGameBar()
            yield PlutoniumWebsiteBar()
            yield plutonium_logger

    def on_mount(self):
        self.main_vertical_scroll_box.styles.margin = 0
        self.main_vertical_scroll_box.styles.padding = 0
        self.main_vertical_scroll_box.styles.border = ("solid", "grey")
        set_theme(app_instance=self, theme_name="dracula")


def configure_app():
    set_window_title(app.TITLE)

    # 52x60 columns/rows in terminal
    set_terminal_size(app, 420, 680)




def run_main_app():

    configure_app()

    app.run()


app = PlutoniumLauncher()
