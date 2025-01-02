from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Label, Static, Input
from textual.screen import Screen

import textual_fspicker

from plutonium_launcher_tui.settings import set_username, get_current_preferred_theme
from plutonium_launcher_tui.customization import set_terminal_size, set_theme, set_window_title
from plutonium_launcher_tui import logger
from plutonium_launcher_tui.base_widgets import (
    BasePlutoniumLauncherHorizontalBox, 
    BasePlutoniumLauncherButton, 
    BasePlutoniumLauncherLabel
)
from plutonium_launcher_tui.plutonium_launcher_widgets import (
    PlutoniumGameAutoExecuteBar,
    PlutoniumGameBar,
    PlutoniumGameSection,
    PlutoniumGameSpecificArgsSection,
    PlutoniumGlobalArgsSection,
    PlutoniumUserBar,
    PlutoniumWebsiteBar,
)


class ConfirmUserNameButton(Static):
    def compose(self) -> ComposeResult:
        self.confirm_button = BasePlutoniumLauncherButton(button_text='Confirm')
        yield self.confirm_button

    def on_mount(self):
        self.confirm_button.styles.width = 'auto'
        self.styles.width = 'auto'
        self.styles.height = 'auto'

    def on_button_pressed(self) -> None:
        text_value = self.parent.parent.parent.text_input.value
        if not text_value or text_value.strip() == '':
            app.user_bar.refresh(recompose=True)
            logger.print_to_log_window('You cannot add a blank username')
            app.pop_screen()
            return
    
        set_username(self.parent.parent.parent.text_input.value)
        self.parent.parent.parent.text_input.value = ''
        app.user_bar.refresh(recompose=True)
        app.pop_screen()
 

class CancelUserNameButton(Static):
    def compose(self) -> ComposeResult:
        self.cancel_button = BasePlutoniumLauncherButton(button_text='Cancel')
        yield self.cancel_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.cancel_button.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        self.parent.parent.parent.text_input.value = ''
        app.pop_screen()


class UsernameInput(Static):
    def compose(self) -> ComposeResult:
        self.label = BasePlutoniumLauncherLabel(label_text='Input your new username', label_border=('hidden', 'grey'), label_padding=(0, 0, 1, 0))
        self.text_input = Input()
        self.vertical_scrollbox = VerticalScroll()
        self.horizontal_bar = BasePlutoniumLauncherHorizontalBox(padding=0)
        self.cancel_button = CancelUserNameButton()
        self.confirm_button = ConfirmUserNameButton()
        with self.vertical_scrollbox:
            yield self.label
            with self.horizontal_bar:
                yield self.text_input
                yield self.cancel_button
                yield self.confirm_button
            yield self.horizontal_bar
        yield self.vertical_scrollbox

    def on_mount(self):
        self.label.styles.width = '100%'
        self.horizontal_bar.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.content_align = ('center', 'middle')
        self.text_input.styles.width = '1fr'
        self.horizontal_bar.styles.border = ('solid', 'grey')


class ScreenZero(Screen):
    def compose(self) -> ComposeResult:
        self.header = Header()
        self.username_input = UsernameInput()
        self.vertical_scroll = VerticalScroll()
        with self.vertical_scroll:
            yield self.header
            yield self.username_input
        yield self.vertical_scroll

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")
        self.vertical_scroll.styles.align = ('center', 'middle')


class ScreenOne(Screen):
    def compose(self) -> ComposeResult:
        self.test = Label('test')
        self.header = Header()
        self.vertical_scroll = VerticalScroll()
        with self.vertical_scroll:
            yield self.header
            yield self.test
        yield self.vertical_scroll

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")


class PlutoniumLauncher(App):
    TITLE = "Plutonium Launcher"

    def compose(self) -> ComposeResult:
        self.screen_zero = ScreenZero()
        self.screen_one = ScreenOne()
        self.main_vertical_scroll_box_zero = VerticalScroll()
        self.plutonium_game_section = PlutoniumGameSection()
        self.user_bar = PlutoniumUserBar()
        with self.main_vertical_scroll_box_zero:
            yield Header()
            yield self.plutonium_game_section
            yield self.user_bar
            yield PlutoniumGlobalArgsSection()
            yield PlutoniumGameSpecificArgsSection()
            yield PlutoniumGameAutoExecuteBar()
            yield PlutoniumGameBar()
            yield PlutoniumWebsiteBar()
            yield logger.plutonium_logger

    def on_mount(self):
        self.install_screen(self.screen_zero, name="screen_zero")
        self.install_screen(self.screen_one, name="screen_one")
        logger.plutonium_logger.styles.height = "1fr"
        logger.plutonium_logger.styles.min_height = 6
        self.main_vertical_scroll_box_zero.styles.margin = 0
        self.main_vertical_scroll_box_zero.styles.padding = 0
        self.main_vertical_scroll_box_zero.styles.border = ("solid", "grey")
        set_theme(app_instance=self, theme_name=get_current_preferred_theme())


def configure_app():
    set_window_title(app.TITLE)

    # 52x60 columns/rows in terminal
    set_terminal_size(app, 420, 680)




def run_main_app():

    configure_app()

    app.run()


app = PlutoniumLauncher()
