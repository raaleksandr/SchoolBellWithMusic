import pytest

from PyQt6.QtCore import QTime
from model import SchoolBellModel

class TestModel:

    @pytest.fixture
    def empty_model(self):
        return SchoolBellModel()

    @pytest.fixture
    def model_with_one_record(self):
        model = SchoolBellModel()
        previous_record = \
            dict(start_weekday_index=1, end_weekday_index=1, time=QTime(20, 2, 25), \
                 description='previous record', file_name='previous_sound.mp3')
        model.add_new_record(previous_record)
        return model

    def test_add_new_record_and_was_no_records_before(self, empty_model):
        model = empty_model
        new_record = \
            dict(start_weekday_index=1, end_weekday_index=1, time=QTime(20, 2, 25), \
                 description='test description',file_name='test_sound.mp3')
        model.add_new_record(new_record)

        assert model.records[0] == new_record

    def test_add_new_record_and_existed_records_before_with_other_key(self, model_with_one_record):
        new_record_with_other_key = \
            dict(start_weekday_index=2, end_weekday_index=2, time=QTime(18, 2, 25), \
                 description='test description', file_name='test_sound.mp3')

        model_with_one_record.add_new_record(new_record_with_other_key)

        inserted_record_index = model_with_one_record.find_record_index(new_record_with_other_key)

        assert inserted_record_index >= 0
        assert model_with_one_record.records[inserted_record_index] == new_record_with_other_key

    def test_find_record_index_when_exists(self, model_with_one_record):
        record_to_find = model_with_one_record.records[0]

        found_index = model_with_one_record.find_record_index(record_to_find)

        assert found_index == 0

    def test_find_record_index_when_not_exists(self, model_with_one_record):
        record_which_not_exists = model_with_one_record.records[0].copy()
        record_which_not_exists['time'] = QTime(18, 2, 25)

        found_index = model_with_one_record.find_record_index(record_which_not_exists)

        assert found_index == -1
