from os import listdir
from os.path import isfile, join, splitext

SOUND_EXTENSIONS = ['WAV', 'MP3']

class PlaySoundsFolderPlayer:

    def __init__(self):
        self.stored_folder_positions = []

    def get_sound_files_in_folder(self, folder_name):

        sound_files = []
        for file in listdir(folder_name):
            filename = join(folder_name, file)

            if not isfile(filename):
                continue

            file_extension = splitext(filename)[-1].upper()
            if file_extension in SOUND_EXTENSIONS:
                sound_files.append(filename)

        return sound_files

    def get_next_file_in_folder(self, folder_name):
        result_file = ''

        sound_files = self.get_sound_files_in_folder(folder_name)

        stored_position = self.find_stored_folder_position(folder_name)
        if stored_position:
            found_position = False
            for sound_file in sound_files:

                if found_position:
                    result_file = sound_file

                if sound_file == stored_position['previous_file_name']:
                    found_position = True

        if not result_file:
             result_file = sound_files[0]

        if result_file:
            if stored_position:
                stored_position['previous_file_name'] = result_file
            else:
                new_stored_position_rec = dict(folder_name=folder_name, previous_file_name=result_file)
                self.stored_folder_positions.append(new_stored_position_rec)

        return result_file

    def find_stored_folder_position(self, folder_name):
        for stored_position in self.stored_folder_positions:
            if stored_position['folder_name'] == folder_name:
                return stored_position

        return None