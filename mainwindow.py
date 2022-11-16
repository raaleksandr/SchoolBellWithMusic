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
            self.ui.testPlayMusicFolderPushButton.clicked.connect(self.test_button)
        except Exception as e:
            print(e)

    def addPushButtonClicked(self, event):
        self.controller.handle_new_record_button()

    def test_button(self, event):
        self.controller.test_play_music()

    def makeGridReadOnly(self):
        self.ui.scheduleTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)