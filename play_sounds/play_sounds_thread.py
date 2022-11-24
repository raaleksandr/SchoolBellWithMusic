import time
import datetime

def main_sounds_thread(controller):
    second = -1
    while not controller.thread_requested_to_stop:
        now_second = datetime.datetime.now().second
        if now_second != second:
            controller.perform_play_sounds_actions()
            controller.refresh_clock()
            controller.refresh_playback_status()

        time.sleep(0.1)

    controller.thread_stopped = True