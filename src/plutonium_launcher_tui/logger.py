from textual.widgets import RichLog, Static


class PlutoniumLauncherLog(Static):
    def compose(self):
        self.rich_log = RichLog(wrap=True)
        yield self.rich_log
        return super().compose()

    def mount(self, *widgets, before=None, after=None):
        self.rich_log.styles.height = 8
        self.rich_log.styles.margin = 1
        self.rich_log.styles.border = ("solid", "grey")
        self.rich_log.border_title = "Logging"
        self.rich_log.styles.width = "100%"
        self.rich_log.styles.scrollbar_size_horizontal = 0
        return super().mount(*widgets, before=before, after=after)


    def print_to_log_window(message: str):
        plutonium_logger.rich_log.write(message)


plutonium_logger = PlutoniumLauncherLog()


def print_to_log_window(message: str):
    plutonium_logger.rich_log.write(message)
