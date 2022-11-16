from PyQt6.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
import sys
import traceback
import threading

from mainwindow import MainWindow
from weekly_schedule_edit import WeeklyScheduleEditDialog
from model import SchoolBellModel
from utils import getWeekdayNameByIndex
from play_sounds.play_sounds_controller import PlaySoundsController
from play_sounds.play_sounds_thread import main_sounds_thread


class SchoolBellController:
    def __init__(self, application_argv):
        try:
            self.app = QApplication(sys.argv)
            self.main_window = MainWindow(self)
            self.model = SchoolBellModel()
            self.play_sounds_controller = PlaySoundsController(self.model)
        except Exception as e:
            self.handle_error(e)

    def run_application(self):
        try:
            self.main_window.show()
            self.refresh_grid()
            self.start_play_sounds_thread()
            sys.exit(self.app.exec())
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, exception):
        try:
            print(exception.__traceback__)
            print(traceback.format_exc())
            QMessageBox.critical(self.main_window, "Error", "Error: '" + str(exception) + "'")
        except Exception as e:
            print(e)

    def handle_new_record_button(self):

        try:
            dlg = WeeklyScheduleEditDialog(self)
            button = dlg.exec()

            if not self.isOkKeyPressedInDialog(button):
                return

            new_record = { "description" : dlg.ui.descriptionLineEdit.text(), \
                           "start_weekday_index" : dlg.ui.startWeekdayComboBox.currentIndex(), \
                           "end_weekday_index" : dlg.ui.endWeekdayComboBox.currentIndex(), \
                           "time" : dlg.ui.timeEdit.time(), \
                           "file_name" : dlg.ui.fileNameLineEdit.text() \
                            }

            self.model.add_new_record(new_record)
            self.refresh_grid()

        except Exception as e:
            self.handle_error(e)

    def isOkKeyPressedInDialog(self, dialogResult):
        if dialogResult == 1:
            return True
        else:
            return False

    def refresh_grid(self):

        self.main_window.ui.scheduleTable.setRowCount(0)

        row = 0
        for record in self.model.records:
            self.main_window.ui.scheduleTable.insertRow(row)
            self.main_window.ui.scheduleTable.setItem(row, 0, QTableWidgetItem(self.output_weekdays(record)))
            self.main_window.ui.scheduleTable.setItem(row, 1, QTableWidgetItem(record["time"].toString()))
            self.main_window.ui.scheduleTable.setItem(row, 2, QTableWidgetItem(record["description"]))
            row = row + 1

        #self.main_window.ui.scheduleTable.repaint()

    def output_weekdays(self, record):
        return getWeekdayNameByIndex(record["start_weekday_index"]) + ' - ' + \
               getWeekdayNameByIndex(record["end_weekday_index"])

    def play_sounds_if_time_has_come(self):
        if self.play_sounds_controller.play_if_time_has_come():
            self.main_window.statusBar().showMessage("Sound is playing", 5000)

    def play_sound_file_for_preview(self, file_name_with_full_path):
        self.play_sounds_controller.play_sound_file_by_path(file_name_with_full_path)

    def start_play_sounds_thread(self):
        thread = threading.Timer(1, main_sounds_thread, [self])
        thread.setDaemon(True)
        thread.start()

    def test_play_music(self):
        self.play_sounds_controller.test_play_music()