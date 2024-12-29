from plutonium_launcher_tui.customization import set_terminal_size


def main():
    set_terminal_size(52, 60)
    
    from plutonium_launcher_tui import main_app
    main_app.run_main_app()
