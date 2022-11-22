from PyQt6.QtWidgets import QDialog, QFileDialog

from utils import loadUi

class WeeklyScheduleEditDialog(QDialog):
    def __init__(self, controller):
        self.controller = controller
        self.main_window = controller.controller.main_window
        super().__init__(self.main_window)
        self.ui = loadUi('weekly_schedule_dialog\\weeklyScheduleEditDialog.ui', self)

        self.init_events()

    def exec(self):
        self.refresh_widgets_visibility()
        self.init_sizes()

        return super().exec()

    def init_events(self):
        self.ui.chooseFilePushButton.clicked.connect(self.chooseFilePushButtonClicked)
        self.ui.playSoundPushButton.clicked.connect(self.playSoundPushButtonClicked)
        self.ui.chooseFolderPushButton.clicked.connect(self.chooseFolderPushButtonClicked)

    def init_sizes(self):
        self.set_widget_top_and_preserve_height(self.ui.musicFolderWidget, \
                                                self.ui.singleFileWidget.geometry().top())

        self.set_widget_top_and_preserve_height(self.ui.buttonBox, \
                                                max(self.ui.musicFolderWidget.geometry().bottom(),\
                                                    self.ui.singleFileWidget.geometry().bottom()))

        self.setFixedHeight(self.ui.buttonBox.geometry().bottom() + 5)

    def set_widget_top_and_preserve_height(self, widget, top):
        geometry = widget.geometry()
        saved_height = geometry.height()
        geometry.setTop(top)
        geometry.setHeight(saved_height)
        widget.setGeometry(geometry)

    def refresh_widgets_visibility(self):
        if self.ui.singleFileRadioButton.isChecked():
            self.ui.musicFolderWidget.setVisible(False)
            self.ui.singleFileWidget.setVisible(True)
        else:
            self.ui.musicFolderWidget.setVisible(True)
            self.ui.singleFileWidget.setVisible(False)

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

            self.controller.play_sound_file_for_preview(filename_sound)
        except Exception as e:
            if str(e) == 'ModPlug_Load failed':
                self.main_window.controller.handle_error("Error playing file, check if file has correct format (mp3, "
                                                         "wav etc)")
            else:
                self.main_window.controller.handle_error(e)

    def chooseFolderPushButtonClicked(self):
        directory = QFileDialog.getExistingDirectory(caption='Choose directory')
        if directory:
            self.ui.folderNameLineEdit.setText(directory)

    def accept(self):
        if self.controller.check_values_in_dialog():
            super().accept()