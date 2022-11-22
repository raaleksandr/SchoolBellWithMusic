from weekly_schedule_dialog.weekly_schedule_edit_dialog import WeeklyScheduleEditDialog
from constants import REC_TYPE_SINGLE_FILE, REC_TYPE_MUSIC_FOLDER

class WeeklyScheduleEditController:

    def __init__(self, controller):
        self.controller = controller
        self.model = controller.model
        self.dialog = None
        self.new_record_flag = False
        self.record_old = None

    def handle_add_new_record(self):

        self.new_record_flag = True

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

    def handle_edit_record(self, record_data):

        self.new_record_flag = False
        self.record_old = record_data.copy()

        try:
            self.dialog = WeeklyScheduleEditDialog(self)

            self.set_record_to_dialog_fields(self.record_old)

            button = self.dialog.exec()

            if not self.isOkKeyPressedInDialog(button):
                return False

            new_record = self.get_record_from_dialog_fields()
            self.model.update_record(record_old=self.record_old, record_new=new_record)

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
                      'file_name': self.dialog.ui.fileNameLineEdit.text(), \
                      'active': True
                      }
        else:
            record = {'description': self.dialog.ui.descriptionLineEdit.text(), \
                      'start_weekday_index': self.dialog.ui.startWeekdayComboBox.currentIndex(), \
                      'end_weekday_index': self.dialog.ui.endWeekdayComboBox.currentIndex(), \
                      'start_time': self.dialog.ui.startTimeEdit.time(),
                      'end_time': self.dialog.ui.endTimeEdit.time(),
                      'rec_type': REC_TYPE_MUSIC_FOLDER,
                      'folder_name': self.dialog.ui.folderNameLineEdit.text(), \
                      'active': True
                      }

        if self.record_old:
            record['active'] = self.record_old['active']

        return record

    def set_record_to_dialog_fields(self, record_data):

        self.dialog.ui.descriptionLineEdit.setText(record_data['description'])
        self.dialog.ui.startWeekdayComboBox.setCurrentIndex(record_data['start_weekday_index'])
        self.dialog.ui.endWeekdayComboBox.setCurrentIndex(record_data['end_weekday_index'])

        if record_data['rec_type'] == REC_TYPE_SINGLE_FILE:
            self.dialog.ui.singleFileRadioButton.setChecked(True)
            self.dialog.ui.musicFolderRadioButton.setChecked(False)
            self.dialog.ui.timeEdit.setTime(record_data['start_time'])
            self.dialog.ui.fileNameLineEdit.setText(record_data['file_name'])
        else:
            self.dialog.ui.singleFileRadioButton.setChecked(False)
            self.dialog.ui.musicFolderRadioButton.setChecked(True)
            self.dialog.ui.startTimeEdit.setTime(record_data['start_time'])
            self.dialog.ui.endTimeEdit.setTime(record_data['end_time'])
            self.dialog.ui.folderNameLineEdit.setText(record_data['folder_name'])


    def check_values_in_dialog(self):
        record_new = self.get_record_from_dialog_fields()
        try:
            if self.new_record_flag:
                self.model.check_record_before_insert(record_data=record_new)
            else:
                self.model.check_record_before_update(record_old=self.record_old, record_new=record_new)
            return True
        except Exception as e:
            self.controller.handle_error(e)
            return False