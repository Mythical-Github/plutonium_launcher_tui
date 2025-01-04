from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Header, Input, Static

from plutonium_launcher_tui.base_widgets import (
    BasePlutoniumLauncherButton,
    BasePlutoniumLauncherHorizontalBox,
    BasePlutoniumLauncherLabel,
)
from plutonium_launcher_tui.logger import print_to_log_window
from plutonium_launcher_tui.settings import (
    get_usernames,
    set_username
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
        simulate_confirm_username_button_pressed()


def simulate_cancel_username_button_pressed():
    from plutonium_launcher_tui.main_app import app
    app.username_screen.username_input.text_input.value = ''
    app.pop_screen()


def simulate_confirm_username_button_pressed():
        from plutonium_launcher_tui.main_app import app
        text_value = app.username_screen.username_input.text_input.value

        if not text_value or text_value.strip() == '':
            print_to_log_window('You cannot add a blank username')
        elif text_value in get_usernames():
            print_to_log_window('You cannot add a username that already exists')
        else:
            set_username(text_value)
            
        app.username_screen.username_input.text_input.value = ''
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
        simulate_cancel_username_button_pressed()


class UsernameActualInput(Input):
    @on(Input.Submitted)
    def on_input_changed(self):
        simulate_confirm_username_button_pressed()


class UsernameInput(Static):
    BINDINGS = [
        ("escape", "cancel_username", "Simulates Hitting the Cancel Button")
    ]
    def compose(self) -> ComposeResult:
        self.label = BasePlutoniumLauncherLabel(
            label_text='Input your new username',
            label_border=('hidden', 'grey'),
            label_padding=(0, 0, 1, 0)
        )
        self.text_input = UsernameActualInput()
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
        
        self.parent.parent.set_focus(self.text_input)

    def action_cancel_username(self):
        simulate_cancel_username_button_pressed()

class UsernameScreen(Screen):
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
