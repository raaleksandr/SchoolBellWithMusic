from weekly_schedule_dialog.weekly_schedule_edit_dialog import WeeklyScheduleEditDialog
from constants import REC_TYPE_SINGLE_FILE, REC_TYPE_MUSIC_FOLDER

class WeeklyScheduleEditController:

    def __init__(self, controller):
        self.controller = controller
        self.model = controller.model
        self.dialog = None

    def handle_add_new_record(self):

        try:
            self.dialog = WeeklyScheduleEditDialog(self)
            button = self.dialog.exec()

            if not self.isOkKeyPressedInDialog(button):
                return False

            new_record = self.get_record_from_dialog_fields()
            self.model.add_new_record(new_record)

            return True

        except Exception as e:
            self.controller.handle_error(e)

    def isOkKeyPressedInDialog(self, dialogResult):
        if dialogResult == 1:
            return True
        else:
            return False

    def get_record_from_dialog_fields(self):
        if self.dialog.ui.singleFileRadioButton.isChecked():
            record = {'description': self.dialog.ui.descriptionLineEdit.text(), \
                      'start_weekday_index': self.dialog.ui.startWeekdayComboBox.currentIndex(), \
                      'end_weekday_index': self.dialog.ui.endWeekdayComboBox.currentIndex(), \
                      'start_time': self.dialog.ui.timeEdit.time(), \
                      'rec_type': REC_TYPE_SINGLE_FILE, \
                      'file_name': self.dialog.ui.fileNameLineEdit.text() \
                      }
        else:
            record = {'description': self.dialog.ui.descriptionLineEdit.text(), \
                      'start_weekday_index': self.dialog.ui.startWeekdayComboBox.currentIndex(), \
                      'end_weekday_index': self.dialog.ui.endWeekdayComboBox.currentIndex(), \
                      'start_time': self.dialog.ui.startTimeEdit.time(),
                      'end_time': self.dialog.ui.endTimeEdit.time(),
                      'rec_type': REC_TYPE_MUSIC_FOLDER,
                      'folder_name': self.dialog.ui.folderNameLineEdit.text() \
                      }

        return record

    def check_values_in_dialog(self):
        record = self.get_record_from_dialog_fields()
        try:
            self.model.check_record(record)
            return True
        except Exception as e:
            self.controller.handle_error(e)
            return False