import pygame
import time

class PlaySoundsModel:

    def __init__(self):
        self.pygame = pygame
        self.pygame.mixer.init()
        self.initialized = True

    def play_the_sound(self, path_to_sound_file):
        try:
            self.pygame.mixer.music.load(path_to_sound_file)
            self.pygame.mixer.music.play()
        except Exception as e:
            if str(e) == 'ModPlug_Load failed':
                raise Exception("Error playing file, check if file has correct format (mp3, wav etc)")
            else:
                raise Exception("Error playing sound file") from e

    def play_files_as_carusel(self, files):

        def wait_music_finished():
            while self.pygame.mixer.music.get_busy():
                time.sleep(1)

        wait_music_finished()
        for file in files:
            self.pygame.mixer.music.load(file)
            self.pygame.mixer.music.play()
            time.sleep(3)
            self.pygame.mixer.music.stop()
            wait_music_finished()

    def is_something_playing(self):
        if self.initialized:
            return self.pygame.mixer.music.get_busy()
        else:
            return False

    def stop_all_sounds(self):
        if self.is_something_playing():
            self.pygame.mixer.music.stop()

    def uninitialize_before_close(self):
        self.pygame.mixer.music.stop()
        self.pygame.mixer.quit()
        self.pygame.quit()
        self.initialized = False