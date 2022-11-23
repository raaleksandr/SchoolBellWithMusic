from PyQt6.QtWidgets import QDialog
import webbrowser

from utils import loadUi


class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = loadUi('about_dialog.ui', self)
        self.ui.openGithubPushButton.clicked.connect(self.click_url)

    def click_url(self):
        webbrowser.open('https://github.com/raaleksandr/SchoolBellWithMusic', new=2)