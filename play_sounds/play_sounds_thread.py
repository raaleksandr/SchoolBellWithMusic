import time

def main_sounds_thread(controller):
    while True:
        controller.perform_play_sounds_actions()
        time.sleep(1)