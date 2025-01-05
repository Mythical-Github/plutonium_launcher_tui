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


class ConfirmButton(Static):
    def __init__(
        self,
        confirm_function
    ):
        super().__init__()
        self.confirm_function = confirm_function
    def compose(self) -> ComposeResult:
        self.confirm_button = BasePlutoniumLauncherButton(button_text='Confirm')
        yield self.confirm_button

    def on_mount(self):
        self.confirm_button.styles.width = 'auto'
        self.styles.width = 'auto'
        self.styles.height = 'auto'
    
    def on_button_pressed(self) -> None:
        simulate_confirm_button_pressed(self.confirm_function)
        post_confirm_button_pressed()


main_text_input = None
def get_screen_text_input():
    global main_text_input
    return main_text_input


def post_cancel_button_pressed():
    from plutonium_launcher_tui.main_app import app
    get_screen_text_input().value = ''
    app.pop_screen()


def post_confirm_button_pressed():
    from plutonium_launcher_tui.main_app import app
    get_screen_text_input().value = ''
    app.user_bar.refresh(recompose=True)
    app.pop_screen()


def simulate_cancel_button_pressed(function):
    function(get_screen_text_input())


def simulate_confirm_button_pressed(function):
    function(get_screen_text_input())

    

class CancelButton(Static):
    def __init__(
        self,
        cancel_function
    ):
        super().__init__()
        self.cancel_function = cancel_function
    def compose(self) -> ComposeResult:
        self.cancel_button = BasePlutoniumLauncherButton(button_text='Cancel')
        yield self.cancel_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.cancel_button.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        simulate_cancel_button_pressed(self.cancel_function)
        post_cancel_button_pressed()


class TextInputScreenInput(Input):
    def __init__(
        self,
        confirm_function
    ):
        super().__init__()
        self.confirm_function = confirm_function
    @on(Input.Submitted)
    def on_input_changed(self):
        simulate_confirm_button_pressed(self.confirm_function)
        post_confirm_button_pressed()


class TextInputMainLayout(Static):
    def __init__(
        self,
        cancel_function,
        confirm_function,
        input_name
    ):
        super().__init__()
        self.cancel_function = cancel_function
        self.confirm_function = confirm_function
        self.input_name = input_name
    BINDINGS = [
        ("escape", "cancel", "Simulates hitting the cancel button")
    ]
    def compose(self) -> ComposeResult:
        self.label = BasePlutoniumLauncherLabel(
            label_text=f'Input the {self.input_name}',
            label_border=('hidden', 'grey'),
            label_padding=(0, 0, 1, 0)
        )
        self.text_input = TextInputScreenInput(self.confirm_function)
        self.vertical_scrollbox = VerticalScroll()
        self.horizontal_bar = BasePlutoniumLauncherHorizontalBox(padding=0)
        self.cancel_button = CancelButton(self.cancel_function)
        self.confirm_button = ConfirmButton(self.confirm_function)
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

        global main_text_input
        main_text_input = self.text_input

    def action_cancel(self):
        simulate_cancel_button_pressed(self.cancel_function)
        post_cancel_button_pressed()


class TextInputScreen(Screen):
    def __init__(
        self,
        cancel_function,
        confirm_function,
        input_name
    ):
        super().__init__()
        self.cancel_function = cancel_function
        self.confirm_function = confirm_function
        self.input_name = input_name

    def compose(self) -> ComposeResult:
        self.header = Header()
        self.text_input_main_layout = TextInputMainLayout(self.cancel_function, self.confirm_function, self.input_name)
        self.vertical_scroll = VerticalScroll()
        with self.vertical_scroll:
            yield self.header
            yield self.text_input_main_layout
        yield self.vertical_scroll

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")
        self.vertical_scroll.styles.align = ('center', 'middle')
