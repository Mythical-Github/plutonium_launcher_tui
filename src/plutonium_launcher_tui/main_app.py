
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header

from plutonium_launcher_tui import logger
from plutonium_launcher_tui.auto_run_thread import start_periodic_check_thread
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
from plutonium_launcher_tui.settings import get_auto_run_game, get_current_preferred_theme, get_title_for_app


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
        self.username_screen = usernames_screen.UsernameScreen(widget_to_refresh=self.user_bar)
        self.game_directory_screen = game_directory_screen.GameDirectoryScreen(widget_to_refresh=self.game_dir_select)
        self.game_args_screen = game_args_screen.GameArgsScreen(widget_to_refresh=self.game_args_section)
        self.global_args_screen = global_args_screen.GlobalArgsScreen(widget_to_refresh=self.global_args_section)
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
    start_periodic_check_thread()
    app.run()

app = PlutoniumLauncher()
