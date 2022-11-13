class SchoolBellModel:
    def __init__(self):
        self.records = []

    def add_new_record(self, record_data):

        if self.check_record_exists(record_data):
            raise Exception("Record with the same days and time already exists")

        new_record = { "start_weekday_index" : record_data["start_weekday_index"], \
                       "end_weekday_index" : record_data["end_weekday_index"], \
                       "time" : record_data["time"], \
                       "description" : record_data["description"], \
                       "file_name" : record_data["file_name"], \
                       "active" : True }
        self.records.append(record_data)

    def find_record_index(self, record_data):
        index = 0
        for rec in self.records:
            if rec["start_weekday_index"] == record_data["start_weekday_index"] \
                and rec["end_weekday_index"] == record_data["end_weekday_index"] \
                and rec["time"] == record_data["time"]:

                return index
            index = index + 1

        return -1

    def check_record_exists(self, record_data):
        return self.find_record_index(record_data) >= 0