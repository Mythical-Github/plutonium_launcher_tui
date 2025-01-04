from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header

from plutonium_launcher_tui import logger
from plutonium_launcher_tui.customization import (
    set_terminal_size, 
    set_window_title
)
from plutonium_launcher_tui.screens import (
    usernames_screen, 
    game_args_screen,
    game_directory_screen,
    global_args_screen
)
from plutonium_launcher_tui.plutonium_launcher_widgets import (
    PlutoniumGameAutoExecuteBar,
    PlutoniumGameBar,
    PlutoniumGameSection,
    PlutoniumGameSpecificArgsSection,
    PlutoniumGlobalArgsSection,
    PlutoniumUserBar,
    PlutoniumWebsiteBar
)
from plutonium_launcher_tui.settings import get_current_preferred_theme


class PlutoniumLauncher(App):
    TITLE = "Plutonium Launcher"

    def compose(self) -> ComposeResult:
        self.username_screen = usernames_screen.UsernameScreen()
        self.game_directory_screen = game_directory_screen.GameDirectoryScreen()
        self.game_args_screen = game_args_screen.GameArgsScreen()
        self.global_args_screen = global_args_screen.GlobalArgsScreen()
        self.main_vertical_scroll_box_zero = VerticalScroll()
        self.plutonium_game_section = PlutoniumGameSection()
        self.user_bar = PlutoniumUserBar()
        self.global_args_section = PlutoniumGlobalArgsSection()
        self.game_args_section = PlutoniumGameSpecificArgsSection()
        with self.main_vertical_scroll_box_zero:
            yield Header()
            yield self.plutonium_game_section
            yield self.user_bar
            yield self.global_args_section
            yield self.game_args_section
            yield PlutoniumGameAutoExecuteBar()
            yield PlutoniumGameBar()
            yield PlutoniumWebsiteBar()
            yield logger.plutonium_logger

    def on_mount(self):
        self.install_screen(self.username_screen, name="username_screen")
        self.install_screen(self.global_args_screen, name='global_args_screen')
        self.install_screen(self.game_args_screen, name='game_args_screen')
        self.install_screen(self.game_directory_screen, name='game_directory_screen')
        self.main_vertical_scroll_box_zero.styles.margin = 0
        self.main_vertical_scroll_box_zero.styles.padding = 0
        self.main_vertical_scroll_box_zero.styles.border = ("solid", "grey")
        self.theme = get_current_preferred_theme()


def configure_app():
    set_window_title(app.TITLE)

    # 52x60 columns/rows in terminal
    set_terminal_size(app, 420, 680)


def run_main_app():
    configure_app()
    app.run()

app = PlutoniumLauncher()
