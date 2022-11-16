import datetime

from play_sounds.play_sounds_model import PlaySoundsModel

class PlaySoundsController:
    def __init__(self, model):
        self.model = model
        self.already_played_records = []
        self.play_sounds_model = PlaySoundsModel()

    def play_if_time_has_come(self):
        is_played = False
        for rec in self.model.records:

            if self.already_played_recently(rec):
                continue

            if not self.check_weekday_matches(rec):
                continue

            if not self.time_has_come(rec):
                continue

            self.play_the_sound(rec)
            is_played = True

        return is_played

    def check_weekday_matches(self, rec):
        weekday = datetime.datetime.now().weekday()
        return ( weekday >= rec['start_weekday_index'] \
            and weekday <= rec['end_weekday_index'] )

    def time_has_come(self, rec):
        time_from_rec = rec['time'].toPyTime()
        current_time = datetime.datetime.now().time()
        diff_time = self.get_time_difference_in_seconds_time1_minus_time2(current_time, time_from_rec)
        if diff_time >= 0 and diff_time <= 5:
            return True
        else:
            return False

    def already_played_recently(self, rec):

        for already_played in self.already_played_records:
            if self.compare_records(already_played, rec):
                if self.how_many_minutes_ago_played(already_played) < 10:
                    return True

        return False

    def compare_records(self, rec1, rec2):
        return ( rec1['start_weekday_index'] == rec2['start_weekday_index'] \
                    and rec1['end_weekday_index'] == rec2['end_weekday_index'] \
                    and rec1['time'] == rec2['time'] )

    def how_many_minutes_ago_played(self, already_played_record):
        time_diff = datetime.datetime.now() - already_played_record['played_date_time']
        return time_diff.total_seconds() / 60

    def play_the_sound(self, rec):

        self.play_sound_file_by_path(rec['file_name'])
        new_already_played_rec = {'start_weekday_index': rec['start_weekday_index'], \
                                  'end_weekday_index': rec['end_weekday_index'], \
                                  'time': rec['time'], \
                                  'played_date_time': datetime.datetime.now()}

        self.already_played_records.append(new_already_played_rec)

    def play_sound_file_by_path(self, full_path_to_sound_file):
        self.play_sounds_model.play_the_sound(full_path_to_sound_file)

    @staticmethod
    def get_time_difference_in_seconds_time1_minus_time2(time1, time2):
        dateTime1 = datetime.datetime.combine(datetime.datetime.now().date(), time1)
        dateTime2 = datetime.datetime.combine(datetime.datetime.now().date(), time2)

        dateTimeDifference = dateTime1 - dateTime2

        return dateTimeDifference.total_seconds()

    def test_play_music(self):
        files = []
        #files.append(r'E:\asana\myprogs\python\desktop\SchoolBell\sounds\bell1.mp3')
        #files.append(r'E:\asana\myprogs\python\desktop\SchoolBell\sounds\bell2.mp3')
        #files.append(r'E:\asana\myprogs\python\desktop\SchoolBell\sounds\bell3.mp3')
        files.append(r'D:\_toarchive\tmp\school-bell\sound_files_for_test\Recording1.mp3')
        files.append(r'D:\_toarchive\tmp\school-bell\sound_files_for_test\Recording2.mp3')
        files.append(r'D:\_toarchive\tmp\school-bell\sound_files_for_test\Recording3.mp3')
        self.play_sounds_model.play_files_as_carusel(files)