import os

from constants import REC_TYPE_SINGLE_FILE, REC_TYPE_MUSIC_FOLDER
from play_sounds.test_play_sounds_folder import PlaySoundsFolderPlayer

class SchoolBellModel:
    def __init__(self):
        self.records = []

    def add_new_record(self, record_data):

        #if self.check_record_exists(record_data):
        #    raise Exception("Record with the same days and time already exists")

        new_record = dict(start_weekday_index=record_data['start_weekday_index'],\
                          end_weekday_index=record_data['end_weekday_index'],\
                          start_time=record_data['start_time'],\
                          rec_type=record_data['rec_type'],\
                          description=record_data['description'],
                          active=True)

        if record_data['rec_type'] == REC_TYPE_SINGLE_FILE:
            new_record['file_name'] = record_data['file_name']
        else:
            new_record['end_time'] = record_data['end_time']
            new_record['folder_name'] = record_data['folder_name']

        self.check_record(new_record)

        self.records.append(new_record)

    def find_record_index(self, record_data):
        index = 0
        for rec in self.records:
            if rec["start_weekday_index"] == record_data["start_weekday_index"] \
                and rec["end_weekday_index"] == record_data["end_weekday_index"] \
                and rec["start_time"] == record_data["start_time"]:

                return index
            index = index + 1

        return -1

    def check_record_exists(self, record_data):
        return self.find_record_index(record_data) >= 0

    def check_record(self, record_data):
        if self.check_record_exists(record_data):
            raise Exception("Record with the same days and time already exists")

        if record_data['start_weekday_index'] > record_data['end_weekday_index']:
            raise Exception("Start week day must be earlier than end week day")

        if record_data['rec_type'] == REC_TYPE_SINGLE_FILE:
            self.specific_checks_when_record_is_single_file(record_data)
        else:
            self.specific_checks_when_record_is_music_folder(record_data)


    def specific_checks_when_record_is_single_file(self, record_data):
        file_name = record_data['file_name']
        if not file_name:
            raise Exception("Enter sound file name")

        if not self.check_file_correct(file_name):
            raise Exception("File is not correct: " + file_name)

    def specific_checks_when_record_is_music_folder(self, record_data):

        start_time = record_data['start_time']
        end_time = record_data['end_time']

        if end_time < start_time:
            raise Exception("End time must be later than start time")

        folder_name = record_data['folder_name']
        if not folder_name:
            raise Exception("Enter folder with music")

        folder_player = PlaySoundsFolderPlayer()
        sound_files_in_folder = folder_player.get_sound_files_in_folder(folder_name)
        if not sound_files_in_folder:
            raise Exception("Folder contains no sound or music files: " + folder_name)

    def check_file_correct(self, file_name):
        return os.path.isfile(file_name)