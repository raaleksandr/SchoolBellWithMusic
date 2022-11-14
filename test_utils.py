from utils import getWeekdayNameByIndex

class TestGetWeekdayNameByIndex:
    def test_monday(self):
        assert getWeekdayNameByIndex(0) == 'Monday'

    def test_friday(self):
        assert getWeekdayNameByIndex(4) == 'Friday'

    def test_sunday(self):
        assert getWeekdayNameByIndex(6) == 'Sunday'