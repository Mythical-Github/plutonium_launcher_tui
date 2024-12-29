from textual.widgets import Header
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll

from plutonium_launcher_tui.customization import set_theme, set_window_title
from plutonium_launcher_tui.logger import plutonium_logger
from plutonium_launcher_tui.plutonium_launcher_widgets import (
    PlutoniumGameAutoExecuteBar,
    PlutoniumGameBar,
    PlutoniumGameSection,
    PlutoniumUserBar,
    PlutoniumGameSpecificArgsSection,
    PlutoniumGlobalArgsSection,
    PlutoniumWebsiteBar
)


class PlutoniumLauncher(App):
    TITLE = 'Plutonium Launcher'
    def compose(self) -> ComposeResult:
        self.main_vertical_scroll_box = VerticalScroll()
        with self.main_vertical_scroll_box:
            yield Header()
            yield PlutoniumGameSection()
            yield PlutoniumUserBar()
            yield PlutoniumGameSpecificArgsSection()
            yield PlutoniumGlobalArgsSection()
            yield PlutoniumGameAutoExecuteBar()
            yield PlutoniumGameBar()
            yield PlutoniumWebsiteBar()
            yield plutonium_logger
            

    def on_mount(self):
        self.main_vertical_scroll_box.styles.margin = (0)
        self.main_vertical_scroll_box.styles.padding = (0)
        self.main_vertical_scroll_box.styles.border = ('solid', 'grey')

        set_theme(app_instance=self, theme_name='dracula')


app = PlutoniumLauncher()

set_window_title(app.TITLE)

app.run()
