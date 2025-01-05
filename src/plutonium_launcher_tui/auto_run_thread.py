import threading
import time

from plutonium_launcher_tui import game_runner
from plutonium_launcher_tui.settings import get_auto_run_game_delay, get_auto_run_game


check_condition_thread = None
stop_thread_event = threading.Event()

time_passed = 0.0
last_run_time = 0.0
TOLERANCE = 0.1
MAX_RUN_INTERVAL = 1.0


def action_on_condition():
    print("Condition met! Performing action...")
    if get_auto_run_game():

        game_runner.run_game()

def periodic_check():
    global time_passed, last_run_time
    while not stop_thread_event.is_set():
        if abs(time_passed - get_auto_run_game_delay()) < TOLERANCE:
            current_time = time.time()
            if current_time - last_run_time >= MAX_RUN_INTERVAL:
                action_on_condition()
                last_run_time = current_time
        time.sleep(0.1)
        time_passed = time_passed + 0.1


def start_periodic_check_thread():
    global check_condition_thread, stop_thread_event
    if check_condition_thread and check_condition_thread.is_alive():
        print("Thread is already running.")
        return

    stop_thread_event.clear()
    check_condition_thread = threading.Thread(target=periodic_check, daemon=True)
    check_condition_thread.start()
    print("Thread started.")


def stop_periodic_check_thread():
    global stop_thread_event
    stop_thread_event.set()
    if check_condition_thread:
        check_condition_thread.join()
    print("Thread stopped.")
