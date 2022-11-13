import pygame

class PlaySoundsModel:

    def __init__(self):
        self.pygame = pygame
        self.pygame.mixer.init()

    def play_the_sound(self,path_to_sound_file):
        try:
            self.pygame.mixer.music.load(path_to_sound_file)
            self.pygame.mixer.music.play()
        except Exception as e:
            if str(e) == 'ModPlug_Load failed':
                raise Exception("Error playing file, check if file has correct format (mp3, wav etc)")
            else:
                raise Exception("Error playing sound file") from e
