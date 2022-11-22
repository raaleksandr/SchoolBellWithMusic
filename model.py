import os
import json
from PyQt6.QtCore import QTime

from constants import REC_TYPE_SINGLE_FILE
from play_sounds.test_play_sounds_folder import PlaySoundsFolderPlayer

INDEX_NOT_FOUND = -1

class SchoolBellModel:
    def __init__(self, file_name_to_store_records):
        self.records = []
        self.file_name_to_store_records = file_name_to_store_records

    def add_new_record(self, record_data):

        new_record = dict(start_weekday_index=record_data['start_weekday_index'],
                          end_weekday_index=record_data['end_weekday_index'],
                          start_time=record_data['start_time'],
                          rec_type=record_data['rec_type'],
                          description=record_data['description'],
                          active=record_data['active'])

        if record_data['rec_type'] == REC_TYPE_SINGLE_FILE:
            new_record['file_name'] = record_data['file_name']
        else:
            new_record['end_time'] = record_data['end_time']
            new_record['folder_name'] = record_data['folder_name']

        self.check_record_before_insert(new_record)
        self.records.append(new_record)

    def update_record(self, record_old, record_new):
        self.check_record_before_update(record_old=record_old, record_new=record_new)
        index_of_old_record = self.find_record_index(record_old)

        if index_of_old_record == INDEX_NOT_FOUND:
            raise Exception('Error updating record, old record does not exist' + str(record_old))

        if self.compare_record_key(record_old, record_new):
            self.records[index_of_old_record] = record_new.copy()
        else:
            self.records.pop(index_of_old_record)
            self.add_new_record(record_new)

    def delete_record(self, record_data):
        index_of_record = self.find_record_index(record_data)
        if index_of_record == INDEX_NOT_FOUND:
            raise Exception('Error deleting record, record not found')

        self.records.pop(index_of_record)

    def find_record_index(self, record_data):
        index = 0
        for rec in self.records:
            if self.compare_record_key(rec, record_data):
                return index

            index = index + 1

        return INDEX_NOT_FOUND

    def find_record(self, record_data):
        record_index = self.find_record_index(record_data)
        if record_index >= 0:
            return self.records[record_index]
        else:
            return None

    def check_record_exists(self, record_data):
        return self.find_record_index(record_data) >= 0

    def compare_record_key(self, record1, record2):
        return ( record1["start_weekday_index"] == record2["start_weekday_index"]
                    and record1["end_weekday_index"] == record2["end_weekday_index"]
                    and record1["start_time"] == record2["start_time"] )

    def check_record_before_insert(self, record_data):
        if self.check_record_exists(record_data):
            raise Exception("Record with the same days and time already exists")

        self.check_record_fields(record_data)

    def check_record_before_update(self, record_old, record_new):
        self.check_record_fields(record_new)

    def check_record_fields(self, record_data):
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

    def save_records_to_file(self):

        dthandler = lambda obj: \
            obj.toString('hh:mm:ss') \
                if isinstance(obj, QTime) else json.JSONEncoder().default(obj)

        records_in_json = json.dumps(self.records, default=dthandler, indent=4)
        file = open(self.file_name_to_store_records, 'w')
        file.write(records_in_json)
        file.close()

    def load_records_from_file(self):
        if not self.check_file_correct(self.file_name_to_store_records):
            return

        file = open(self.file_name_to_store_records)
        lines = file.readlines()
        file.close()

        all_file_as_string = ''.join(lines)

        loaded_records = json.loads(all_file_as_string)

        self.records.clear()

        def convert_field_to_QTime(dict, field_name):
            if not field_name in dict.keys():
                return

            value_not_converted = dict[field_name]
            value_converted = QTime.fromString(value_not_converted, 'hh:mm:ss')
            dict[field_name] = value_converted

        for loaded_rec in loaded_records:
            convert_field_to_QTime(loaded_rec, 'start_time')
            convert_field_to_QTime(loaded_rec, 'end_time')

            self.add_new_record(loaded_rec)


