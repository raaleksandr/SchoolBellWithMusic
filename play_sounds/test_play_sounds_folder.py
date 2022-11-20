import pytest

from play_sounds.play_sounds_folder import PlaySoundsFolderPlayer

class TestPlaySoundsFolder:
    @pytest.fixture
    def any_folder_contains_those_files(self, mocker, files_list):
        playsound_folder_mock = \
            mocker.patch('play_sounds.play_sounds_folder.PlaySoundsFolderPlayer.get_sound_files_in_folder')

        playsound_folder_mock.return_value = files_list

    @pytest.mark.parametrize('files_list', [['file_test1.mp3']])
    def test_get_next_file_first_time(self, any_folder_contains_those_files):
        cut = PlaySoundsFolderPlayer()
        result = cut.get_next_file_in_folder('folder1')
        assert result == 'file_test1.mp3'

    @pytest.mark.parametrize('files_list', [['file_test1.mp3', 'file_test2.mp3']])
    def test_get_next_file_second_time(self, any_folder_contains_those_files):
        cut = PlaySoundsFolderPlayer()

        cut.get_next_file_in_folder('folder1')
        result = cut.get_next_file_in_folder('folder1')
        assert result == 'file_test2.mp3'

    @pytest.mark.parametrize('files_list', [['file_test1.mp3', 'file_test2.mp3']])
    def test_get_next_file_start_from_beginning(self, any_folder_contains_those_files):
        cut = PlaySoundsFolderPlayer()

        cut.get_next_file_in_folder('folder1')
        cut.get_next_file_in_folder('folder1')
        result = cut.get_next_file_in_folder('folder1')
        assert result == 'file_test1.mp3'

    @pytest.mark.parametrize('files_list', [['file_test1.mp3', 'file_test2.mp3', 'file_test3.mp3']])
    def test_get_next_file_second_time_when_there_are_3_files(self, any_folder_contains_those_files):
        cut = PlaySoundsFolderPlayer()

        cut.get_next_file_in_folder('folder1')
        result = cut.get_next_file_in_folder('folder1')
        assert result == 'file_test2.mp3'

    @pytest.mark.parametrize('files_list', [['file_test1.mp3', 'file_test2.mp3']])
    def test_get_next_file_different_folder(self, any_folder_contains_those_files):
        cut = PlaySoundsFolderPlayer()

        cut.get_next_file_in_folder('folder1')
        result = cut.get_next_file_in_folder('folder2')
        assert result == 'file_test1.mp3'

    @pytest.mark.parametrize('files_list', [[]])
    def test_case_when_folder_is_empty(self, any_folder_contains_those_files):
        cut = PlaySoundsFolderPlayer()

        cut.get_next_file_in_folder('folder1')
        result = cut.get_next_file_in_folder('folder2')
        assert result == ''