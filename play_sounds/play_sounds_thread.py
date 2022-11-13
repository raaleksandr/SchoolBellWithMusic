import time

def main_sounds_thread(controller):
    while True:
        controller.play_sounds_if_time_has_come()
        time.sleep(1)
        #print('imhere')