from PyQt6.QtWidgets import QMainWindow, QTableWidget

from utils import loadUi

class MainWindow(QMainWindow):
    def __init__(self, controller):
        try:
            super().__init__()
            self.controller = controller
            self.ui = loadUi('mainwindow.ui', self)
            self.makeGridReadOnly()

            self.ui.addPushButton.clicked.connect(self.addPushButtonClicked)
        except Exception as e:
            print(e)

    def addPushButtonClicked(self, event):
        self.controller.handle_new_record_button()

    def makeGridReadOnly(self):
        self.ui.scheduleTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)