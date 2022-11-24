import datetime

from play_sounds.play_sounds_model import PlaySoundsModel
from play_sounds.play_sounds_folder import PlaySoundsFolderPlayer
from constants import REC_TYPE_SINGLE_FILE, REC_TYPE_MUSIC_FOLDER

class PlaySoundsController:
    def __init__(self, controller):
        self.controller = controller
        self.model = self.controller.model
        self.playback_history = []
        self.play_sounds_model = PlaySoundsModel()
        self.folder_play = PlaySoundsFolderPlayer()

    def perform_play_sounds_actions(self):
        something_started_to_play = False
        for rec in self.active_records():

            if not self.rec_must_play(rec):
                continue

            try:
                self.play_the_sound(rec)
                something_started_to_play = True
            except Exception as e:
                self.controller.handle_error(e)

        if not something_started_to_play:
            if self.some_music_from_folder_still_plays_but_should_not():
                self.stop_all_sounds()

    def active_records(self):
        records_act = []
        for rec in self.model.records:
            if rec['active'] == True:
                records_act.append(rec)

        return records_act


    def rec_must_play(self, rec):

        if not self.check_weekday_matches(rec):
            return False

        if rec['rec_type'] == REC_TYPE_SINGLE_FILE:
            if self.rec_played_recently(rec):
                return False

            if not self.time_has_come(rec):
                return False
        else:
            if not self.time_in_range_of_rec(rec):
                return False

            if self.is_something_playing():
                return False

        return True

    def check_weekday_matches(self, rec):
        weekday = datetime.datetime.now().weekday()
        return ( weekday >= rec['start_weekday_index'] \
            and weekday <= rec['end_weekday_index'] )

    def time_has_come(self, rec):
        time_from_rec = rec['start_time'].toPyTime()
        current_time = datetime.datetime.now().time()
        diff_time = self.get_time_difference_in_seconds_time1_minus_time2(current_time, time_from_rec)
        if diff_time >= 0 and diff_time <= 5:
            return True
        else:
            return False

    def rec_played_recently(self, rec):

        for history_rec in self.playback_history:
            if self.compare_records(history_rec, rec):
                if self.how_many_minutes_ago_played(history_rec) < 10:
                    return True

        return False

    def time_in_range_of_rec(self, rec):
        start_time_from_rec = rec['start_time'].toPyTime()
        end_time_from_rec = rec['end_time'].toPyTime()
        current_time = datetime.datetime.now().time()
        if current_time >= start_time_from_rec and current_time <= end_time_from_rec:
            return True
        else:
            return False

    def compare_records(self, rec1, rec2):
        return ( rec1['start_weekday_index'] == rec2['start_weekday_index'] \
                    and rec1['end_weekday_index'] == rec2['end_weekday_index'] \
                    and rec1['start_time'] == rec2['start_time'] )

    def how_many_minutes_ago_played(self, history_record):
        time_diff = datetime.datetime.now() - history_record['played_date_time']
        return time_diff.total_seconds() / 60

    def play_the_sound(self, rec):

        filename = ''
        if rec['rec_type'] == REC_TYPE_SINGLE_FILE:
            filename = rec['file_name']
        else:
            folder_name = rec['folder_name']
            filename = self.folder_play.get_next_file_in_folder(folder_name)

            if not filename:
                raise Exception('Folder ' + folder_name + ' contains no sound files')

        if filename:
            self.play_sound_file_by_path(filename)

        self.add_history_rec(rec)

    def add_history_rec(self, rec):
        new_history_rec = dict(start_weekday_index=rec['start_weekday_index'],\
                               end_weekday_index=rec['end_weekday_index'],\
                               start_time=rec['start_time'],\
                               played_date_time=datetime.datetime.now(),\
                               scheduled_rec=rec.copy())

        self.playback_history.append(new_history_rec)

    def play_sound_file_by_path(self, full_path_to_sound_file):
        self.play_sounds_model.play_the_sound(full_path_to_sound_file)

    @staticmethod
    def get_time_difference_in_seconds_time1_minus_time2(time1, time2):
        dateTime1 = datetime.datetime.combine(datetime.datetime.now().date(), time1)
        dateTime2 = datetime.datetime.combine(datetime.datetime.now().date(), time2)

        dateTimeDifference = dateTime1 - dateTime2

        return dateTimeDifference.total_seconds()

    def is_something_playing(self):
        return self.play_sounds_model.is_something_playing()

    def any_music_folder_must_play_now(self):
        for rec in self.active_records():
            if rec['rec_type'] != REC_TYPE_MUSIC_FOLDER:
                continue

            if self.time_in_range_of_rec(rec):
                return True

        return False

    def stop_all_sounds(self):
        self.play_sounds_model.stop_all_sounds()

    def get_last_history_record_that_was_played(self):
        if self.playback_history:
            return self.playback_history[-1]['scheduled_rec']
        else:
            return None

    def last_that_played_was_music_folder(self):
        last_history_record = self.get_last_history_record_that_was_played()
        if not last_history_record:
            return False

        return ( last_history_record['rec_type'] == REC_TYPE_MUSIC_FOLDER )

    def some_music_from_folder_still_plays_but_should_not(self):
        if ( not self.any_music_folder_must_play_now() ) \
             and self.is_something_playing() \
             and self.last_that_played_was_music_folder():

            return True
        else:
            return False

    def uninitialize_before_close(self):
        self.play_sounds_model.uninitialize_before_close()

    def test_play_music(self):
        files = []
        files.append(r'D:\_toarchive\tmp\school-bell\sound_files_for_test\Recording1.mp3')
        files.append(r'D:\_toarchive\tmp\school-bell\sound_files_for_test\Recording2.mp3')
        files.append(r'D:\_toarchive\tmp\school-bell\sound_files_for_test\Recording3.mp3')
        self.play_sounds_model.play_files_as_carusel(files)