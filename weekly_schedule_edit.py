from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6 import uic
import pygame

from utils import loadUi

class WeeklyScheduleEditDialog(QDialog):
    def __init__(self, parentWindow):
        super().__init__(parentWindow)
        self.main_window = parentWindow
        self.ui = loadUi('weeklyScheduleEditDialog.ui', self)
        #self.ui = uic.loadUi('weeklyScheduleEditDialog.ui', self)
        #self.ui = uic.loadUi(r'E:\asana\myprogs\python\desktop\SchoolBell\weeklyScheduleEditDialog.ui', self)

        self.ui.chooseFilePushButton.clicked.connect(self.chooseFilePushButtonClicked)
        self.ui.playSoundPushButton.clicked.connect(self.playSoundPushButtonClicked)

        pygame.mixer.init()

    def chooseFilePushButtonClicked(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            if fname[0]:
                self.ui.fileNameLineEdit.setText(fname[0])
        except Exception as e:
            print(e)

    def playSoundPushButtonClicked(self):

        try:
            #filename_sound = self.ui.fileNameLineEdit.getText()
            filename_sound = self.ui.fileNameLineEdit.text()
            if filename_sound == '':
                return

            pygame.mixer.music.load(filename_sound)
            pygame.mixer.music.play()
            #while pygame.mixer.music.get_busy():
            #    pygame.time.Clock().tick(10)
        except Exception as e:
            if str(e) == 'ModPlug_Load failed':
                self.main_window.controller.handle_error('Error playing file, check if file has correct format (mp3, wav etc)')
            else:
                self.main_window.controller.handle_error(e)