class SchoolBellModel:
    def __init__(self):
        self.records = []

    def add_new_record(self, record_data):

        if self.check_record_exists(record_data):
            raise Exception("Record with the same days and time already exists")

        new_record = { 'start_weekday_index' : record_data['start_weekday_index'], \
                       'end_weekday_index' : record_data['end_weekday_index'], \
                       'start_time' : record_data['start_time'], \
                       'end_time' : record_data['end_time'], \
                       'rec_type' : record_data['rec_type'], \
                       'description' : record_data['description'], \
                       'file_name' : record_data['file_name'], \
                       'active' : True }
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