from PyQt6.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
import sys

from mainwindow import MainWindow
from weekly_schedule_edit import WeeklyScheduleEditDialog
from model import SchoolBellModel

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

            new_record = { "start_weekday_index" : dlg.ui.startWeekdayComboBox.currentIndex(), \
                           "end_weekday_index" : dlg.ui.endWeekdayComboBox.currentIndex(), \
                           "time" : dlg.ui.timeEdit.time(), \
                           "description" : "dummy" }

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

        #row = 0
        #self.main_window.ui.scheduleTable.setRowCount(50)
        #self.main_window.ui.scheduleTable.insertRow(0)
        #self.main_window.ui.scheduleTable.setItem(row, 0, QTableWidgetItem("test1"))
        #self.main_window.ui.scheduleTable.setItem(row, 1, QTableWidgetItem("test2"))
        #self.main_window.ui.scheduleTable.setItem(row, 2, QTableWidgetItem("test3"))

        row = 0
        for record in self.model.records:
            self.main_window.ui.scheduleTable.insertRow(row)
            self.main_window.ui.scheduleTable.setItem(row, 0, QTableWidgetItem(record["start_weekday_index"]))
            self.main_window.ui.scheduleTable.setItem(row, 1, QTableWidgetItem(str(record["time"])))
            self.main_window.ui.scheduleTable.setItem(row, 2, QTableWidgetItem(record["description"]))
            row = row + 1

        self.main_window.ui.scheduleTable.repaint()