import pytest

import datetime
from datetime import date
from PyQt6.QtCore import QTime
from datetime import datetime as datetime_attr

from play_sounds.play_sounds_controller import PlaySoundsController
from controller import SchoolBellController
import test_model
from constants import REC_TYPE_SINGLE_FILE, REC_TYPE_MUSIC_FOLDER

class TestPlaySoundsController:

    @pytest.fixture
    def empty_controller_with_empty_model(self):
        controller = SchoolBellController()
        play_sounds_controller = PlaySoundsController(controller)
        return play_sounds_controller

    def test_get_time_difference_in_seconds_time1_minus_time2(self):
        time1 = datetime.time(20, 5, 10)
        time2 = datetime.time(20, 5, 5)

        difference = PlaySoundsController.get_time_difference_in_seconds_time1_minus_time2(time1, time2)

        assert difference == 5

    def test_play_the_sound(self, mocker, empty_controller_with_empty_model):
        cut = empty_controller_with_empty_model

        rec_to_play = dict(start_weekday_index=1, end_weekday_index=1, start_time=QTime(7, 20, 25), \
                           rec_type=REC_TYPE_SINGLE_FILE, file_name='testfile.mp3')
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_the_sound(rec_to_play)

        playsound_mock.assert_called_once_with('testfile.mp3')
        self.assert_recs_have_equal_key(rec_to_play, cut.playback_history[0])

    def assert_recs_have_equal_key(self, rec1, rec2):
        assert rec1['start_weekday_index'] == rec2['start_weekday_index']
        assert rec1['end_weekday_index'] == rec2['end_weekday_index']
        assert rec1['start_time'] == rec2['start_time']

CORRECT_TIME_HOUR = 23
CORRECT_TIME_MINUTE = 55
DUMMY_DATE = '01.01.1900'

class TestPlaySoundsControllerMethod_perform_play_sounds_actions:

    @pytest.fixture
    def switch_off_file_correctness_check(self, mocker):
        check_file_correct_mock = mocker.patch('model.SchoolBellModel.check_file_correct')
        check_file_correct_mock.return_value = True

    @pytest.fixture
    def patch_datetime_now_weekday(self, monkeypatch, fake_system_date):
        fake_now_date_as_object = datetime.datetime.strptime(fake_system_date['date'], "%d.%m.%Y").date()
        parsed_rec_time = parse_time(fake_system_date['time'])
        fake_now_time_as_object = datetime.time(parsed_rec_time['hour'], parsed_rec_time['minute'], \
                                                parsed_rec_time['second'])

        class mock_now:
            @classmethod
            def weekday(cls):
                return fake_system_date['weekday']

            @classmethod
            def time(cls):
                return fake_now_time_as_object

            @classmethod
            def date(cls):
                return fake_now_date_as_object

            def __sub__(self, other_member):
                this_object_date_time = datetime_attr.combine(fake_now_date_as_object,
                                                              fake_now_time_as_object)
                return this_object_date_time - other_member

        class mock_datetime:
            @classmethod
            def now(cls):
                return mock_now()

            @classmethod
            def combine(cls, date_arg, time_arg):
                return datetime_attr.combine(date_arg, time_arg)

            @classmethod
            def date(cls, year_arg, month_arg, date_arg):
                return date(year_arg, month_arg, date_arg)

        monkeypatch.setattr(datetime, 'datetime', mock_datetime)

    @pytest.fixture
    def patch_that_a_sound_is_already_playing(self, mocker):
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.is_something_playing')
        playsound_mock.return_value = True

    def compose_playback_history_rec(self, weekday, time_as_string, played_date_time_as_string, rec_type):
        time_split_at_hour_minute = parse_time(time_as_string)
        played_date_time = datetime_attr.strptime(played_date_time_as_string, '%d.%m.%Y %H:%M:%S')
        start_time_as_Qtime = QTime(time_split_at_hour_minute['hour'], time_split_at_hour_minute['minute'],\
                                    time_split_at_hour_minute['second'])

        scheduled_rec = dict(start_weekday_index=weekday,end_weekday_index=weekday, \
                            start_time = start_time_as_Qtime, rec_type= rec_type)

        return dict(start_weekday_index=weekday, end_weekday_index=weekday, \
                    start_time=start_time_as_Qtime, played_date_time=played_date_time, \
                    scheduled_rec=scheduled_rec)

class TestPlaySoundsControllerPlaySingleFile(TestPlaySoundsControllerMethod_perform_play_sounds_actions):
    @pytest.fixture
    def controller_with_test_recs_in_model(self, switch_off_file_correctness_check, scheduled_rec_time):
        controller = SchoolBellController()

        parsed_rec_time = parse_time(scheduled_rec_time)

        model_record = \
            dict(start_weekday_index=1, end_weekday_index=1, \
                 start_time=QTime(parsed_rec_time['hour'], parsed_rec_time['minute'], parsed_rec_time['second']), \
                 rec_type=REC_TYPE_SINGLE_FILE, description='test record', file_name='test_sound.mp3', \
                 active=True)

        controller.model.add_new_record(model_record)

        play_sounds_controller = PlaySoundsController(controller)
        return play_sounds_controller

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:55:00', weekday=1)])
    def test_ring_time_equals(self, mocker, controller_with_test_recs_in_model, patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.perform_play_sounds_actions()

        playsound_mock.assert_called_once_with('test_sound.mp3')

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:50:00', weekday=1)])
    def test_not_rings_time_less_5min(self, mocker, controller_with_test_recs_in_model, patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.perform_play_sounds_actions()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:54:57', weekday=1)])
    def test_not_rings_time_less_3sec(self, mocker, controller_with_test_recs_in_model, patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.perform_play_sounds_actions()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:55:00', weekday=2)])
    def test_not_rings_another_week(self, mocker, controller_with_test_recs_in_model, patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.perform_play_sounds_actions()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_system_date', [dict(date='15.11.2022', time='23:55:00', weekday=1)])
    def test_not_rings_because_already_played(self, mocker, controller_with_test_recs_in_model, \
                                              patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playback_history_rec = \
            self.compose_playback_history_rec(weekday=1, time_as_string='23:55:00',\
                                              played_date_time_as_string='15.11.2022 23:54:00',\
                                              rec_type=REC_TYPE_SINGLE_FILE)
        cut.playback_history.append(playback_history_rec)

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.perform_play_sounds_actions()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_system_date', [dict(date='15.11.2022', time='23:57:00', weekday=1)])
    def test_not_rings_time_is_more(self, mocker, controller_with_test_recs_in_model, \
                                              patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.perform_play_sounds_actions()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_system_date', [dict(date='15.11.2022', time='23:55:01', weekday=1)])
    def test_single_file_must_not_be_stopped_until_it_ends(self, mocker, controller_with_test_recs_in_model, \
                                                           patch_datetime_now_weekday, \
                                                           patch_that_a_sound_is_already_playing):
        cut = controller_with_test_recs_in_model

        mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        playback_history_rec = \
            self.compose_playback_history_rec(weekday=1, time_as_string='23:55:00',\
                                              played_date_time_as_string='15.11.2022 23:54:00',\
                                              rec_type=REC_TYPE_SINGLE_FILE)
        cut.playback_history.append(playback_history_rec)

        stopsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.stop_all_sounds')

        cut.perform_play_sounds_actions()

        stopsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:55:00', weekday=1)])
    def test_not_ring_because_record_not_active(self, mocker, controller_with_test_recs_in_model, \
                                                patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model
        cut.model.records[0]['active'] = False

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.perform_play_sounds_actions()

        playsound_mock.assert_not_called()

class TestPlaySoundsControllerPlayMusicFolder(TestPlaySoundsControllerMethod_perform_play_sounds_actions):

    def patch_files_in_folder(self, mocker, files_list):
        playsound_folder_mock = \
            mocker.patch('play_sounds.play_sounds_folder.PlaySoundsFolderPlayer.get_sound_files_in_folder')

        playsound_folder_mock.return_value = files_list

    @pytest.fixture
    def patch_files_in_folder_fixture(self, mocker, files_list):
        self.patch_files_in_folder(mocker, files_list)

    @pytest.fixture
    def controller_with_test_recs_in_model(self, patch_files_in_folder_fixture, scheduled_rec):
        controller = SchoolBellController()
        model = controller.model

        parsed_rec_start = parse_time(scheduled_rec['start'])
        parsed_rec_end = parse_time(scheduled_rec['end'])

        model_record = \
            dict(start_weekday_index=scheduled_rec['weekday'], end_weekday_index=scheduled_rec['weekday'], \
                 start_time=QTime(parsed_rec_start['hour'], parsed_rec_start['minute'], parsed_rec_start['second']), \
                 end_time=QTime(parsed_rec_end['hour'], parsed_rec_end['minute'], parsed_rec_end['second']), \
                 rec_type=REC_TYPE_MUSIC_FOLDER, description='test record', folder_name=scheduled_rec['folder'], \
                 active=True)
        model.add_new_record(model_record)

        play_sounds_controller = PlaySoundsController(controller)
        return play_sounds_controller

    @pytest.mark.parametrize('scheduled_rec', \
                             [dict(start='23:00:00', end='23:05:00', weekday=1, folder=r'C:\test_folder')])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:00:00', weekday=1)])
    @pytest.mark.parametrize('files_list', [['test_file1.mp3']])
    def test_plays_time_equals_start(self, mocker, controller_with_test_recs_in_model, \
                                     patch_datetime_now_weekday):

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        controller_with_test_recs_in_model.perform_play_sounds_actions()

        playsound_mock.assert_called_once_with('test_file1.mp3')

    @pytest.mark.parametrize('scheduled_rec', \
                             [dict(start='23:00:00', end='23:05:00', weekday=1, folder=r'C:\test_folder')])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:03:00', weekday=1)])
    @pytest.mark.parametrize('files_list', [['test_file1.mp3']])
    def test_plays_time_between_start_and_end(self, mocker, controller_with_test_recs_in_model, \
                                              patch_datetime_now_weekday):
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        controller_with_test_recs_in_model.perform_play_sounds_actions()

        playsound_mock.assert_called_once_with('test_file1.mp3')

    @pytest.mark.parametrize('scheduled_rec', \
                             [dict(start='23:00:00', end='23:05:00', weekday=1, folder=r'C:\test_folder')])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:06:00', weekday=1)])
    @pytest.mark.parametrize('files_list', [['test_file1.mp3']])
    def test_doesnt_play_time_more_than_end(self, mocker, controller_with_test_recs_in_model, \
                                                  patch_datetime_now_weekday):

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        controller_with_test_recs_in_model.perform_play_sounds_actions()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec', \
                             [dict(start='23:00:00', end='23:05:00', weekday=1, folder=r'C:\test_folder')])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:01:00', weekday=1)])
    @pytest.mark.parametrize('files_list', [['test_file1.mp3']])
    def test_doesnt_play_because_is_already_playing_now(self, mocker, controller_with_test_recs_in_model, \
                                                        patch_datetime_now_weekday, \
                                                        patch_that_a_sound_is_already_playing):

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        controller_with_test_recs_in_model.perform_play_sounds_actions()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec', \
                             [dict(start='23:00:00', end='23:05:00', weekday=1, folder=r'C:\test_folder')])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:01:00', weekday=1)])
    @pytest.mark.parametrize('files_list', [['test_file1.mp3', 'test_file2.mp3']])
    def test_play_second_file_when_first_finished(self, mocker, controller_with_test_recs_in_model, \
                                                  patch_datetime_now_weekday):

        cut = controller_with_test_recs_in_model
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.folder_play.get_next_file_in_folder(r'C:\test_folder')

        cut.perform_play_sounds_actions()

        playsound_mock.assert_called_once_with('test_file2.mp3')

    @pytest.mark.parametrize('scheduled_rec', \
                             [dict(start='23:00:00', end='23:05:00', weekday=1, folder=r'C:\test_folder')])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:05:01', weekday=1)])
    @pytest.mark.parametrize('files_list', [['test_file1.mp3']])
    def test_stop_music_from_folder_when_time_is_up(self, mocker, controller_with_test_recs_in_model, \
                                                    patch_datetime_now_weekday, \
                                                    patch_that_a_sound_is_already_playing):
        cut = controller_with_test_recs_in_model
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')
        stopsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.stop_all_sounds')

        history_rec = \
            self.compose_playback_history_rec(weekday=1, time_as_string='23:00:00', \
                                              played_date_time_as_string='15.11.2022 23:00:00', \
                                              rec_type=REC_TYPE_MUSIC_FOLDER)
        cut.playback_history.append(history_rec)

        cut.perform_play_sounds_actions()

        stopsound_mock.assert_called_once()

    @pytest.mark.parametrize('scheduled_rec', \
                             [dict(start='23:00:00', end='23:05:00', weekday=1, folder=r'C:\test_folder')])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:04:01', weekday=1)])
    @pytest.mark.parametrize('files_list', [['test_file1.mp3']])
    def test_dont_stop_single_file_even_if_time_in_range(self, mocker, controller_with_test_recs_in_model, \
                                                         patch_datetime_now_weekday, \
                                                         patch_that_a_sound_is_already_playing):
        cut = controller_with_test_recs_in_model
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')
        stopsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.stop_all_sounds')

        history_rec = \
            self.compose_playback_history_rec(weekday=1, time_as_string='23:04:00', \
                                              played_date_time_as_string='15.11.2022 23:04:00', \
                                              rec_type=REC_TYPE_SINGLE_FILE)
        cut.playback_history.append(history_rec)

        cut.perform_play_sounds_actions()

        stopsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec', \
                             [dict(start='23:00:00', end='23:05:00', weekday=1, folder=r'C:\test_folder')])
    @pytest.mark.parametrize('fake_system_date', [dict(date=DUMMY_DATE, time='23:01:00', weekday=1)])
    @pytest.mark.parametrize('files_list', [['some_file_delete_in_test.mp3']])
    def test_if_folder_contains_no_sound_files_then_report_error(self, mocker, controller_with_test_recs_in_model, \
                                                                 patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')
        handle_error_mock = mocker.patch('controller.SchoolBellController.handle_error')

        self.patch_files_in_folder(mocker, [])

        cut.perform_play_sounds_actions()

        playsound_mock.assert_not_called()
        handle_error_mock.assert_called_once()

def parse_time(time_as_string):
    splitted_value_str = time_as_string.split(':')
    splitted_value_int = []
    for one_value_str in splitted_value_str:
        splitted_value_int.append(int(one_value_str))

    return_value = dict(hour=splitted_value_int[0], minute=splitted_value_int[1], \
                        second=splitted_value_int[2])
    return return_value