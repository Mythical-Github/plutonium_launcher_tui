
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header

from plutonium_launcher_tui import logger
from plutonium_launcher_tui import auto_run_thread
from plutonium_launcher_tui.customization import set_terminal_size, set_window_title
from plutonium_launcher_tui.plutonium_launcher_widgets import (
    PlutoniumGameAutoExecuteBar,
    PlutoniumGameBar,
    PlutoniumGameDirectoryBar,
    PlutoniumGameModeSelector,
    PlutoniumGameSelector,
    PlutoniumGameSpecificArgsSection,
    PlutoniumGlobalArgsSection,
    PlutoniumUserBar,
    PlutoniumWebsiteBar,
)
from plutonium_launcher_tui.screens import game_args_screen, game_directory_screen, global_args_screen, usernames_screen
from plutonium_launcher_tui.settings import get_current_preferred_theme, get_title_for_app

has_initially_set_theme = False

class PlutoniumLauncher(App):
    TITLE = get_title_for_app()
    def compose(self) -> ComposeResult:
        self.main_vertical_scroll_box_zero = VerticalScroll()
        self.game_selector = PlutoniumGameSelector()
        self.game_mode_selector = PlutoniumGameModeSelector()
        self.game_dir_select = PlutoniumGameDirectoryBar()
        self.user_bar = PlutoniumUserBar()
        self.global_args_section = PlutoniumGlobalArgsSection()
        self.game_args_section = PlutoniumGameSpecificArgsSection()
        with self.main_vertical_scroll_box_zero:
            yield Header()
            yield self.game_selector
            yield self.game_mode_selector
            yield self.game_dir_select
            yield self.user_bar
            yield self.global_args_section
            yield self.game_args_section
            yield PlutoniumGameAutoExecuteBar()
            yield PlutoniumGameBar()
            yield PlutoniumWebsiteBar()
            yield logger.plutonium_logger

    def on_mount(self):
        self.main_vertical_scroll_box_zero.styles.margin = 0
        self.main_vertical_scroll_box_zero.styles.padding = 0
        self.main_vertical_scroll_box_zero.styles.border = ("solid", "grey")
        self.theme = get_current_preferred_theme()
        auto_run_thread.has_initially_set_theme = True


def configure_app():
    set_window_title(app.TITLE)

    # 52x60 columns/rows in terminal
    set_terminal_size(app, 420, 680)


def run_main_app():
    configure_app()
    auto_run_thread.start_periodic_check_thread(app)
    app.run()


app = PlutoniumLauncher()
