from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from weekly_schedule_edit import WeeklyScheduleEditDialog

class MainWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.ui = uic.loadUi('mainwindow.ui', self)

            self.ui.addPushButton.clicked.connect(self.addPushButtonClicked)
        except Exception as e:
            print(e)

    def addPushButtonClicked(self, event):
        #print(event)
        try:
            dlg = WeeklyScheduleEditDialog(self)
            button = dlg.exec()

            if self.isOkKeyPressedInDialog(button):
                print('OK button pressed')

            print(dlg.ui.startWeekdayComboBox.currentIndex())

        except Exception as e:
            print(e)

    def isOkKeyPressedInDialog(self,dialogResult):
        if dialogResult == 1:
            return True
        else:
            return False