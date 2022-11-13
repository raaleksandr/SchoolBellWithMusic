from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
import pygame

from utils import loadUi

class WeeklyScheduleEditDialog(QDialog):
    def __init__(self, controller):
        self.controller = controller
        self.main_window = controller.main_window
        super().__init__(self.main_window)
        self.ui = loadUi('weeklyScheduleEditDialog.ui', self)

        self.ui.chooseFilePushButton.clicked.connect(self.chooseFilePushButtonClicked)
        self.ui.playSoundPushButton.clicked.connect(self.playSoundPushButtonClicked)

        #pygame.mixer.init()

    def chooseFilePushButtonClicked(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            if fname[0]:
                self.ui.fileNameLineEdit.setText(fname[0])
        except Exception as e:
            print(e)

    def playSoundPushButtonClicked(self):

        try:
            filename_sound = self.ui.fileNameLineEdit.text()
            if filename_sound == '':
                return

            #pygame.mixer.music.load(filename_sound)
            #pygame.mixer.music.play()
            self.controller.play_sound_file_for_preview(filename_sound)
        except Exception as e:
            if str(e) == 'ModPlug_Load failed':
                self.main_window.controller.handle_error("Error playing file, check if file has correct format (mp3, "
                                                         "wav etc)")
            else:
                self.main_window.controller.handle_error(e)