from PyQt6.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
import PyQt6.QtCore as QtCore

import sys
import traceback
import threading
import datetime
import time

import constants
from mainwindow import MainWindow
from model import SchoolBellModel
from utils import getWeekdayNameByIndex, getWeekdayIndexByName, loadIcon
from play_sounds.play_sounds_controller import PlaySoundsController
from play_sounds.play_sounds_thread import main_sounds_thread
from weekly_schedule_dialog.weekly_schedule_edit_controller import WeeklyScheduleEditController
from about_dialog import AboutDialog

class SchoolBellController:
    def __init__(self):
        try:
            self.model = SchoolBellModel(constants.FILE_NAME_TO_SAVE_RECORDS)
            self.play_sounds_controller = PlaySoundsController(self)
            self.weekly_schedule_edit_controller = WeeklyScheduleEditController(self)
            self.grid_is_refreshing = False
            self.thread_requested_to_stop = False
            self.thread_stopped = False

        except Exception as e:
            self.handle_error(e)

    def run_application(self, application_argv):
        try:
            self.app = QApplication(application_argv)
            self.app.setWindowIcon(loadIcon('icon\school_bell_icon.ico'))
            self.main_window = MainWindow(self)
            self.main_window.show()
            self.refresh_clock()
            self.model.load_records_from_file()
            self.refresh_grid()
            self.set_default_column_width()
            self.start_play_sounds_thread()
            sys.exit(self.app.exec())
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, exception):
        try:
            print(exception.__traceback__)
            print(traceback.format_exc())
            QMessageBox.critical(self.main_window, "Error", "Error: '" + str(exception) + "'")
        except Exception as e:
            print(e)

    def handle_new_record_button(self):
        if self.weekly_schedule_edit_controller.handle_add_new_record():
            self.handle_data_changed()

    def handle_edit_record_button(self):
        selected_record = self.get_selected_record()
        if not selected_record:
            return

        if self.weekly_schedule_edit_controller.handle_edit_record(selected_record):
            self.handle_data_changed()

    def handle_delete_record_button(self):
        selected_record = self.get_selected_record()
        if not selected_record:
            return

        result = QMessageBox.question(self.main_window, "Question", "Do you really want to delete the record?")
        if result == QMessageBox.StandardButton.Yes:
            self.model.delete_record(selected_record)
            self.handle_data_changed()

    def get_selected_record(self):

        selected_indexes = self.main_window.ui.scheduleTable.selectionModel().selectedRows()
        if not selected_indexes:
           return

        selected_index = selected_indexes[0]
        return self.get_record_by_table_widget_index(selected_index)

    def get_record_by_table_widget_index(self, index):

        def get_text_of_column(column_number):
            index_of_column = model.index(index.row(), column_number, QtCore.QModelIndex())
            text_of_column = model.data(index_of_column, QtCore.Qt.ItemDataRole.DisplayRole)
            return text_of_column

        def decode_start_end_week(text_of_week_column):
            splitted = text_of_week_column.split('-')
            start_weekday_index = getWeekdayIndexByName(splitted[0].strip())
            end_weekday_index = getWeekdayIndexByName(splitted[1].strip())
            return start_weekday_index, end_weekday_index

        def decode_start_time(text_of_date_column):
            start_time_as_string = text_of_date_column.split(' ')[0]
            start_time = datetime.datetime.strptime(start_time_as_string, '%H:%M:%S').time()
            return start_time

        model = index.model()
        text_of_week_column = get_text_of_column(1)
        text_of_dates_column = get_text_of_column(2)

        start_weekday_index, end_weekday_index = decode_start_end_week(text_of_week_column)
        start_time = decode_start_time(text_of_dates_column)

        record_data = dict(start_weekday_index=start_weekday_index, end_weekday_index=end_weekday_index,
                           start_time=start_time)

        return self.model.find_record(record_data)

    def handle_data_changed(self):
        self.refresh_grid()
        self.save_changes_to_file()

    def refresh_grid(self):

        self.grid_is_refreshing = True

        self.main_window.ui.scheduleTable.setRowCount(0)

        row = 0
        for record in self.model.records:
            self.main_window.ui.scheduleTable.insertRow(row)

            checkBox = QTableWidgetItem(record['active'])
            checkBox.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled )

            if record['active']:
                checkBox.setCheckState(QtCore.Qt.CheckState.Checked)
            else:
                checkBox.setCheckState(QtCore.Qt.CheckState.Unchecked)

            self.main_window.ui.scheduleTable.setItem(row, 0, checkBox)
            self.main_window.ui.scheduleTable.setItem(row, 1, QTableWidgetItem(self.output_weekdays(record)))
            self.main_window.ui.scheduleTable.setItem(row, 2, QTableWidgetItem(self.output_time(record)))
            self.main_window.ui.scheduleTable.setItem(row, 3, QTableWidgetItem(record["description"]))
            self.main_window.ui.scheduleTable.setItem(row, 4, QTableWidgetItem(self.output_file_folder(record)))
            row = row + 1

        self.main_window.ui.scheduleTable.itemChanged.connect(self.check_box_in_grid_changed)

        self.grid_is_refreshing = False

    def set_default_column_width(self):
        grid = self.main_window.ui.scheduleTable
        grid.setColumnWidth(0, 50)
        grid.setColumnWidth(1, 150)
        grid.setColumnWidth(2, 125)
        grid.setColumnWidth(3, 200)
        grid.setColumnWidth(4, 200)

    def check_box_in_grid_changed(self, item):

        if self.grid_is_refreshing:
            return

        parentTableWidget = item.tableWidget()
        index = parentTableWidget.indexFromItem(item)
        record_data = self.get_record_by_table_widget_index(index)
        record_data_old = record_data.copy()
        record_data_new = record_data.copy()

        if item.checkState() == QtCore.Qt.CheckState.Checked:
            record_data_new['active'] = True
        else:
            record_data_new['active'] = False

        self.model.update_record(record_old=record_data_old, record_new=record_data_new)
        self.save_changes_to_file()

    def save_changes_to_file(self):
        self.model.save_records_to_file()

    def output_weekdays(self, record):
        return getWeekdayNameByIndex(record["start_weekday_index"]) + ' - ' + \
               getWeekdayNameByIndex(record["end_weekday_index"])

    def output_time(self, record):
        if record['rec_type'] == constants.REC_TYPE_SINGLE_FILE:
            return record["start_time"].toString()
        else:
            return record["start_time"].toString() + ' - ' + record["end_time"].toString()
    def output_file_folder(self, record):
        if record['rec_type'] == constants.REC_TYPE_SINGLE_FILE:
            return '1 file: ' + record['file_name']
        else:
            return 'all files in: ' + record['folder_name']

    def perform_play_sounds_actions(self):
        self.play_sounds_controller.perform_play_sounds_actions()

    def play_sound_file_for_preview(self, file_name_with_full_path):
        self.play_sounds_controller.play_sound_file_by_path(file_name_with_full_path)

    def start_play_sounds_thread(self):
        self.thread_requested_to_stop = False
        self.thread = threading.Timer(1, main_sounds_thread, [self])
        self.thread.setDaemon(True)
        self.thread.start()

    def stop_play_sounds_thread(self):
        self.thread_stopped = False
        self.thread_requested_to_stop = True
        while not self.thread_stopped:
            time.sleep(0.3)

    def refresh_clock(self):
        self.main_window.labelClock.setText(datetime.datetime.now().time().strftime('%H:%M:%S'))

    def refresh_playback_status(self):
        if self.play_sounds_controller.is_something_playing():
            self.main_window.labelMessage.setText('Sound is playing')
        else:
            self.main_window.labelMessage.setText('')

    def handle_show_about_dialog(self):
        aboutDialog = AboutDialog()
        aboutDialog.exec()

    def uninitialize_before_close(self):
        self.stop_play_sounds_thread()
        self.play_sounds_controller.uninitialize_before_close()