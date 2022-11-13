from PyQt6.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
import sys

from mainwindow import MainWindow
from weekly_schedule_edit import WeeklyScheduleEditDialog
from model import SchoolBellModel
from utils import getWeekdayNameByIndex

class SchoolBellController:
    def __init__(self, application_argv):
        try:
            self.app = QApplication(sys.argv)
            self.main_window = MainWindow(self)
            self.model = SchoolBellModel()
        except Exception as e:
            self.handle_error(e)

    def run_application(self):
        try:
            self.main_window.show()
            self.refresh_grid()
            sys.exit(self.app.exec())
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, exception):
        try:
            QMessageBox.critical(self.main_window, "Error", "Error: '" + str(exception) + "'");
        except Exception as e:
            print(e)

    def handle_new_record_button(self):
        try:
            dlg = WeeklyScheduleEditDialog(self.main_window)
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