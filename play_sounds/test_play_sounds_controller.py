import pytest

import datetime
from PyQt6.QtCore import QTime

from play_sounds.play_sounds_controller import PlaySoundsController
from model import SchoolBellModel

class TestPlaySoundsController:

    @pytest.fixture
    def empty_controller_with_empty_model(self):
        model = SchoolBellModel()
        play_sounds_controller = PlaySoundsController(model)
        return play_sounds_controller

    def test_get_time_difference_in_seconds_time1_minus_time2(self):
        time1 = datetime.time(20, 5, 10)
        time2 = datetime.time(20, 5, 5)

        difference = PlaySoundsController.get_time_difference_in_seconds_time1_minus_time2(time1, time2)

        assert difference == 5

    def test_play_the_sound(self, mocker, empty_controller_with_empty_model):
        cut = empty_controller_with_empty_model

        rec_to_play = dict(start_weekday_index=1, end_weekday_index=1, time=QTime(20, 2, 25), \
                           file_name='testfile.mp3')
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_the_sound(rec_to_play)

        playsound_mock.assert_called_once_with('testfile.mp3')
        self.assert_recs_have_equal_key(rec_to_play, cut.already_played_records[0])

    def assert_recs_have_equal_key(self, rec1, rec2):
        assert rec1['start_weekday_index'] == rec2['start_weekday_index']
        assert rec1['end_weekday_index'] == rec2['end_weekday_index']
        assert rec1['time'] == rec2['time']

class TestPlaySoundsControllerMethodPlayIfTimeHasCome:
    @pytest.fixture
    def controller_with_test_recs_in_model(self):
        model = SchoolBellModel()

        model_record = \
            dict(start_weekday_index=1, end_weekday_index=1, time=QTime(7, 20, 0), \
                 description='test record', file_name='test_sound.mp3')
        model.add_new_record(model_record)

        play_sounds_controller = PlaySoundsController(model)
        return play_sounds_controller

    @pytest.fixture
    def time_and_weekday_matches(self, mocker):
        datetime_mock = mocker.patch('datetime.datetime.now')
        datetime_mock.return_value = datetime.datetime(2016,4,30,3,20,6)

        time_mock = mocker.patch('datetime.datetime.now.time')
        time_mock.return_value = datetime.time(10,20,0)

        weekday_mock = mocker.patch('datetime.datetime.now.weekday')
        weekday_mock.return_value = 1

    def test_ring_time_equals(self, mocker, controller_with_test_recs_in_model, time_and_weekday_matches):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_if_time_has_come()

        playsound_mock.assert_called_once_with('test_sound.mp3')
