from PyQt6.QtWidgets import QMainWindow, QTableWidget, QLabel
from PyQt6.QtGui import QAction

from utils import loadUi

class MainWindow(QMainWindow):
    def __init__(self, controller):
        try:
            super().__init__()
            self.controller = controller
            self.ui = loadUi('mainwindow.ui', self)
            self.setGridSettings()

            self.ui.addPushButton.clicked.connect(self.addPushButtonClicked)
            self.ui.editPushButton.clicked.connect(self.editPushButtonClicked)
            self.ui.deletePushButton.clicked.connect(self.deletePushButtonClicked)
            self.ui.testPlayMusicFolderPushButton.clicked.connect(self.test_button)

            self.labelClock = QLabel('', self)
            self.ui.statusBar().addPermanentWidget(self.labelClock, 1)

            self.labelMessage = QLabel('', self)
            self.ui.statusBar().addPermanentWidget(self.labelMessage, 3)
            #self.widget = QWidget(self)
            #self.labelMessage = QLabel('', self.widget)
            #self.ui.statusBar().addPermanentWidget(self.widget, 3)

            menu_action = QAction('Option #1', self)
            menu_action.setData('option1')
            menu_action.triggered.connect(self.show_about_dialog)

            #self.ui.actionAbout.addAction(menu_action)
            self.ui.actionAbout.triggered.connect(self.show_about_dialog)

        except Exception as e:
            print(e)

    def addPushButtonClicked(self, event):
        self.controller.handle_new_record_button()

    def editPushButtonClicked(self, event):
        self.controller.handle_edit_record_button()

    def deletePushButtonClicked(self, event):
        self.controller.handle_delete_record_button()

    def test_button(self, event):
        self.controller.test_play_music()

    def setGridSettings(self):
        self.makeGridReadOnly()
        self.allowOnlySingleRowSelection()

    def makeGridReadOnly(self):
        self.ui.scheduleTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def allowOnlySingleRowSelection(self):
        self.ui.scheduleTable.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.ui.scheduleTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def show_about_dialog(self):
        self.controller.handle_show_about_dialog()