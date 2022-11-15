import pytest

import datetime
from datetime import date
from PyQt6.QtCore import QTime
from datetime import datetime as datetime_attr

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

        rec_to_play = dict(start_weekday_index=1, end_weekday_index=1, time=QTime(7, 20, 25), \
                           file_name='testfile.mp3')
        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_the_sound(rec_to_play)

        playsound_mock.assert_called_once_with('testfile.mp3')
        self.assert_recs_have_equal_key(rec_to_play, cut.already_played_records[0])

    def assert_recs_have_equal_key(self, rec1, rec2):
        assert rec1['start_weekday_index'] == rec2['start_weekday_index']
        assert rec1['end_weekday_index'] == rec2['end_weekday_index']
        assert rec1['time'] == rec2['time']

CORRECT_TIME_HOUR = 23
CORRECT_TIME_MINUTE = 55
DUMMY_DATE = '01.01.1900'

class TestPlaySoundsControllerMethodPlayIfTimeHasCome:
    @pytest.fixture
    def controller_with_test_recs_in_model(self, scheduled_rec_time):
        model = SchoolBellModel()

        parsed_rec_time = parse_time(scheduled_rec_time)

        model_record = \
            dict(start_weekday_index=1, end_weekday_index=1, \
                 time=QTime(parsed_rec_time['hour'], parsed_rec_time['minute'], parsed_rec_time['second']), \
                 description='test record', file_name='test_sound.mp3')
        model.add_new_record(model_record)

        play_sounds_controller = PlaySoundsController(model)
        return play_sounds_controller

    @pytest.fixture
    def patch_datetime_now_weekday(self, monkeypatch, fake_now_date, fake_now_time, fake_now_weekday):

        fake_now_date_as_object = datetime.datetime.strptime(fake_now_date, "%d.%m.%Y").date()
        parsed_rec_time = parse_time(fake_now_time)
        fake_now_time_as_object = datetime.time(parsed_rec_time['hour'], parsed_rec_time['minute'], \
                                                parsed_rec_time['second'])

        class mock_now:
            @classmethod
            def weekday(cls):
                return fake_now_weekday

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

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_now_weekday', [1])
    @pytest.mark.parametrize('fake_now_date', [DUMMY_DATE])
    @pytest.mark.parametrize('fake_now_time', ['23:55:00'])
    def test_ring_time_equals(self, mocker, controller_with_test_recs_in_model, patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_if_time_has_come()

        playsound_mock.assert_called_once_with('test_sound.mp3')

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_now_weekday', [1])
    @pytest.mark.parametrize('fake_now_date', [DUMMY_DATE])
    @pytest.mark.parametrize('fake_now_time', ['23:50:00'])
    def test_not_rings_time_less_5min(self, mocker, controller_with_test_recs_in_model, patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_if_time_has_come()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_now_weekday', [1])
    @pytest.mark.parametrize('fake_now_date', [DUMMY_DATE])
    @pytest.mark.parametrize('fake_now_time', ['23:54:57'])
    def test_not_rings_time_less_3sec(self, mocker, controller_with_test_recs_in_model, patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_if_time_has_come()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_now_weekday', [2])
    @pytest.mark.parametrize('fake_now_date', [DUMMY_DATE])
    @pytest.mark.parametrize('fake_now_time', ['23:55:00'])
    def test_not_rings_another_week(self, mocker, controller_with_test_recs_in_model, patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_if_time_has_come()

        playsound_mock.assert_not_called()

    @pytest.mark.parametrize('scheduled_rec_time', ['23:55:00'])
    @pytest.mark.parametrize('fake_now_weekday', [1])
    @pytest.mark.parametrize('fake_now_date', ['15.11.2022'])
    @pytest.mark.parametrize('fake_now_time', ['23:55:00'])
    def test_not_rings_because_already_played(self, mocker, controller_with_test_recs_in_model, \
                                              patch_datetime_now_weekday):
        cut = controller_with_test_recs_in_model

        already_played_rec = self.compose_already_played_rec(1, '23:55:00', '15.11.2022 23:54:00')
        cut.already_played_records.append(already_played_rec)

        playsound_mock = mocker.patch('play_sounds.play_sounds_model.PlaySoundsModel.play_the_sound')

        cut.play_if_time_has_come()

        playsound_mock.assert_not_called()

    def compose_already_played_rec(self, weekday, time_as_string, played_date_time_as_string):
        time_split_at_hour_minute = parse_time(time_as_string)
        played_date_time = datetime_attr.strptime(played_date_time_as_string, '%d.%m.%Y %H:%M:%S')
        return dict(start_weekday_index=weekday, end_weekday_index=weekday, \
                    time=QTime(time_split_at_hour_minute['hour'], time_split_at_hour_minute['minute'],\
                               time_split_at_hour_minute['second']), \
                    played_date_time=played_date_time)

def parse_time(time_as_string):
    splitted_value_str = time_as_string.split(':')
    splitted_value_int = []
    for one_value_str in splitted_value_str:
        splitted_value_int.append(int(one_value_str))

    return_value = dict(hour=splitted_value_int[0], minute=splitted_value_int[1], \
                        second=splitted_value_int[2])
    return return_value