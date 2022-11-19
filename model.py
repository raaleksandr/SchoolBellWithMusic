from constants import REC_TYPE_SINGLE_FILE, REC_TYPE_MUSIC_FOLDER

class SchoolBellModel:
    def __init__(self):
        self.records = []

    def add_new_record(self, record_data):

        if self.check_record_exists(record_data):
            raise Exception("Record with the same days and time already exists")

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