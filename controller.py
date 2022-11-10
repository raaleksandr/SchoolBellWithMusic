from PyQt6.QtWidgets import QApplication, QMessageBox
import sys

from mainwindow import MainWindow

class SchoolBellController:
    def __init__(self, application_argv):
        try:
            self.app = QApplication(sys.argv)
            self.main_window = MainWindow() #self)
        except Exception as e:
            self.handle_error(e)

    def run_application(self):
        try:
            self.main_window.show()
            sys.exit(self.app.exec())
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, exception):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText("Error" + exception)
        dlg.exec()
