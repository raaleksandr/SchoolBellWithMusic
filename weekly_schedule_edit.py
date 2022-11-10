from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6 import uic

class WeeklyScheduleEditDialog(QDialog):
    def __init__(self, parentWindow):
        super().__init__(parentWindow)
        self.ui = uic.loadUi('weeklyScheduleEditDialog.ui', self)

        self.ui.chooseFilePushButton.clicked.connect(self.chooseFilePushButtonClicked)

    def chooseFilePushButtonClicked(self):
        try:
            print("im in choose file")
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            if fname[0]:
                self.ui.fileNameLineEdit.setText(fname[0])
        except Exception as e:
            print(e)