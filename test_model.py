import pytest

from PyQt6.QtCore import QTime
from model import SchoolBellModel
from constants import REC_TYPE_SINGLE_FILE, REC_TYPE_MUSIC_FOLDER

class TestModelParent:
    @pytest.fixture
    def empty_model(self):
        return SchoolBellModel('dummy')

TIME_ALREADY_EXISTED = QTime(20, 2, 25)
ANY_OTHER_TIME = QTime(18, 2, 25)

class TestModelSingleFile(TestModelParent):

    @pytest.fixture
    def all_file_correctness_checks_are_true(self, mocker):
        check_file_correct_mock = mocker.patch('model.SchoolBellModel.check_file_correct')
        check_file_correct_mock.return_value = True

    @pytest.fixture
    def construct_some_test_record(self):
        some_test_record = \
            dict(start_weekday_index=1, end_weekday_index=1, start_time=TIME_ALREADY_EXISTED, \
                 end_time=None, rec_type=REC_TYPE_SINGLE_FILE, \
                 description='previous record', file_name='previous_sound.mp3', active=True)
        return some_test_record

    @pytest.fixture
    def model_with_one_record(self, construct_some_test_record, all_file_correctness_checks_are_true):
        model = SchoolBellModel('dummy')
        previous_record = construct_some_test_record
        model.add_new_record(previous_record)
        return model

    @pytest.fixture
    def all_file_correctness_checks_are_false(self, mocker):
        check_file_correct_mock = mocker.patch('model.SchoolBellModel.check_file_correct')
        check_file_correct_mock.return_value = False

    def test_add_new_record_and_was_no_records_before(self, empty_model, all_file_correctness_checks_are_true):
        model = empty_model
        new_record = \
            dict(start_weekday_index=1, end_weekday_index=1, start_time=ANY_OTHER_TIME, \
                 rec_type=REC_TYPE_SINGLE_FILE, description='test description', file_name='test_sound.mp3', \
                 active=True)
        model.add_new_record(new_record)

        self.assert_records_equal(model.records[0], new_record)

    def test_add_new_record_and_existed_records_before_with_other_key(self, model_with_one_record):
        new_record_with_other_key = \
            dict(start_weekday_index=2, end_weekday_index=2, start_time=ANY_OTHER_TIME, \
                 rec_type=REC_TYPE_SINGLE_FILE, description='test description',\
                 file_name='test_sound.mp3', active=True)

        model_with_one_record.add_new_record(new_record_with_other_key)

        inserted_record_index = model_with_one_record.find_record_index(new_record_with_other_key)

        assert inserted_record_index >= 0
        self.assert_records_equal(model_with_one_record.records[inserted_record_index],new_record_with_other_key)

    def test_find_record_index_when_exists(self, model_with_one_record):
        record_to_find = model_with_one_record.records[0]

        found_index = model_with_one_record.find_record_index(record_to_find)

        assert found_index == 0

    def test_find_record_index_when_not_exists(self, model_with_one_record):
        record_which_not_exists = model_with_one_record.records[0].copy()
        record_which_not_exists['start_time'] = QTime(18, 2, 25)

        found_index = model_with_one_record.find_record_index(record_which_not_exists)

        assert found_index == -1

    def test_error_try_to_add_when_record_already_exists(self, model_with_one_record):
        record_which_exists = model_with_one_record.records[0].copy()

        with pytest.raises(Exception):
            model_with_one_record.add_new_record(record_which_exists)

    def test_error_try_to_add_start_week_more_than_end_week(self, empty_model, construct_some_test_record, \
                                                            all_file_correctness_checks_are_true):
        some_record_with_data = construct_some_test_record
        some_record_with_data['start_weekday_index'] = 2
        some_record_with_data['end_weekday_index'] = 1

        with pytest.raises(Exception):
            empty_model.add_new_record(some_record_with_data)

    def test_error_try_to_add_when_file_is_not_filled(self, empty_model, construct_some_test_record, \
                                                      all_file_correctness_checks_are_true):
        some_record_with_data = construct_some_test_record
        some_record_with_data['file_name'] = ''

        with pytest.raises(Exception):
            empty_model.add_new_record(some_record_with_data)

    def test_error_try_to_add_when_file_is_not_filled(self, empty_model, construct_some_test_record, \
                                                      all_file_correctness_checks_are_true):
        some_record_with_data = construct_some_test_record
        some_record_with_data['file_name'] = ''

        with pytest.raises(Exception):
            empty_model.add_new_record(some_record_with_data)

    def test_error_try_to_add_when_file_is_not_correct(self, empty_model, construct_some_test_record, \
                                                       all_file_correctness_checks_are_false):
        some_record_with_data = construct_some_test_record

        with pytest.raises(Exception):
            empty_model.add_new_record(some_record_with_data)

    def test_update_record_key_not_changes(self, model_with_one_record, all_file_correctness_checks_are_true):

        NEW_FILE_NAME = 'changed_file.mp3'

        record_old = model_with_one_record.records[0]
        record_new = record_old.copy()
        record_new['file_name'] = NEW_FILE_NAME

        model_with_one_record.update_record(record_new=record_new, record_old=record_old)

        assert model_with_one_record.records[0]['file_name'] == NEW_FILE_NAME
        assert len(model_with_one_record.records) == 1

    def test_update_record_key_changes(self, model_with_one_record, all_file_correctness_checks_are_true):

        NEW_FILE_NAME = 'changed_file.mp3'

        record_old = model_with_one_record.records[0]
        record_new = record_old.copy()
        record_new['start_time'] = ANY_OTHER_TIME
        record_new['file_name'] = NEW_FILE_NAME

        model_with_one_record.update_record(record_new=record_new, record_old=record_old)

        assert model_with_one_record.records[0]['start_time'] == ANY_OTHER_TIME
        assert len(model_with_one_record.records) == 1

    def test_error_when_update_and_new_key_exists(self, empty_model, construct_some_test_record, \
                                                  all_file_correctness_checks_are_true):
        ANY_TIME1 = TIME_ALREADY_EXISTED
        ANY_TIME2 = ANY_OTHER_TIME

        cut = empty_model
        def add_2_any_records_to_model():
            record1 = construct_some_test_record.copy()
            record1['start_time'] = ANY_TIME1

            record2 = construct_some_test_record.copy()
            record2['start_time'] = ANY_TIME2

            cut.records.append(record1)
            cut.records.append(record2)

        def try_to_change_start_time_in_one_rec_to_start_time_equal_to_second_rec():
            record_old = cut.records[0].copy()
            record_new = record_old.copy()
            record_new['start_time'] = ANY_TIME2

            cut.update_record(record_new=record_new, record_old=record_old)

        add_2_any_records_to_model()

        with pytest.raises(Exception):
            try_to_change_start_time_in_one_rec_to_start_time_equal_to_second_rec()

    def test_delete_record(self, model_with_one_record):
        cut = model_with_one_record
        record_to_delete = cut.records[0].copy()
        cut.delete_record(record_to_delete)
        assert len(cut.records) == 0

    def assert_records_equal(self, rec1, rec2):
        assert rec1['start_weekday_index'] == rec2['start_weekday_index']
        assert rec1['end_weekday_index'] == rec2['end_weekday_index']
        assert rec1['start_time'] == rec2['start_time']
        assert rec1['description'] == rec2['description']
        assert rec1['file_name'] == rec2['file_name']

class TestModelMusicFolder(TestModelParent):

    @pytest.fixture
    def make_folder_contain_files_to_pass_check(self, mocker):
        mocker_get_sound_files = mocker.patch(\
            'play_sounds.play_sounds_folder.PlaySoundsFolderPlayer.get_sound_files_in_folder')
        mocker_get_sound_files.return_value = ['some_file1.mp3', 'some_file2.mp3']

    @pytest.fixture
    def make_folder_not_containing_files_to_lead_to_error(self, mocker):
        mocker_get_sound_files = mocker.patch( \
            'play_sounds.play_sounds_folder.PlaySoundsFolderPlayer.get_sound_files_in_folder')
        mocker_get_sound_files.return_value = []

    @pytest.fixture
    def construct_some_test_record(self):
        some_test_record = \
            dict(start_weekday_index=1, end_weekday_index=1, start_time=ANY_OTHER_TIME, \
                 end_time=QTime(20, 3, 25), rec_type=REC_TYPE_MUSIC_FOLDER, \
                 description='test description', folder_name='C:\music', active=True)

        return some_test_record

    def test_add_new_record_and_was_no_records_before(self, empty_model, construct_some_test_record, \
                                                      make_folder_contain_files_to_pass_check):
        model = empty_model

        new_record = construct_some_test_record
        model.add_new_record(new_record)

        self.assert_records_equal(model.records[0], new_record)

    def test_error_when_end_time_ealier_when_start_time(self, empty_model, construct_some_test_record, \
                                                        make_folder_contain_files_to_pass_check):

        model = empty_model
        new_record = construct_some_test_record
        new_record['start_time'] = QTime(10, 0, 0)
        new_record['end_time'] = QTime(9, 0, 0)

        with pytest.raises(Exception):
            model.add_new_record(new_record)

    def test_error_when_folder_is_not_filled(self, empty_model, construct_some_test_record, \
                                             make_folder_contain_files_to_pass_check):
        model = empty_model
        new_record = construct_some_test_record
        new_record['folder_name'] = ''

        with pytest.raises(Exception):
            model.add_new_record(new_record)

    def test_error_when_folder_does_not_contain_sound_files(self, empty_model, construct_some_test_record, \
                                                            make_folder_not_containing_files_to_lead_to_error):
        model = empty_model
        new_record = construct_some_test_record

        with pytest.raises(Exception):
            model.add_new_record(new_record)

    def assert_records_equal(self, rec1, rec2):
        assert rec1['start_weekday_index'] == rec2['start_weekday_index']
        assert rec1['end_weekday_index'] == rec2['end_weekday_index']
        assert rec1['start_time'] == rec2['start_time']
        assert rec1['end_time'] == rec2['end_time']
        assert rec1['rec_type'] == rec2['rec_type']
        assert rec1['description'] == rec2['description']
        assert rec1['folder_name'] == rec2['folder_name']