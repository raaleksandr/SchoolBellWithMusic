from os import listdir
from os.path import isfile, join, splitext

SOUND_EXTENSIONS = ['WAV', 'MP3']

class PlaySoundsFolderPlayer:

    def __init__(self):
        self.stored_folder_positions = []

    def get_sound_files_in_folder(self, folder_name):

        def get_extension(filename):
            return splitext(filename)[-1]

        def remove_point_from_extension(file_extension):
            if not file_extension:
                return ''

            if file_extension[0] == '.':
                return file_extension[1:]
            else:
                return file_extension

        sound_files = []
        try:
            for file in listdir(folder_name):
                filename = join(folder_name, file)

                if not isfile(filename):
                    continue

                file_extension = get_extension(filename)
                file_extension = remove_point_from_extension(file_extension)
                file_extension = file_extension.upper()
                if file_extension in SOUND_EXTENSIONS:
                    sound_files.append(filename)
        except:
            sound_files = []

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
                    break

                if sound_file == stored_position['previous_file_name']:
                    found_position = True

        if not result_file:
            if sound_files:
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

    def folder_has_sound_files(self, folder_name):
        sound_files_in_folder = self.get_sound_files_in_folder(folder_name)
        if sound_files_in_folder:
            return True
        else:
            return False