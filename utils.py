import sys, os, calendar

from PyQt6 import uic
from PyQt6 import QtGui

def loadUi(relative_filename, parentWidget):
    ui_filename = correct_filename_if_run_as_exe(relative_filename)
    return uic.loadUi(ui_filename, parentWidget)

def loadIcon(relative_filename):
    icon_filename = correct_filename_if_run_as_exe(relative_filename)
    return QtGui.QIcon(icon_filename)

def correct_filename_if_run_as_exe(filename):
    if isRunFromPyInstallerExeWithOneFileOption():
        corrected_filename = os.path.join(sys._MEIPASS, filename)
    else:
        corrected_filename = filename

    return corrected_filename

def isRunFromPyInstallerExeWithOneFileOption():
    try:
        if sys._MEIPASS:
            return True
        else:
            return False

    except Exception as e:
        return False

def getWeekdayNameByIndex(weekdayIndex):
    return list(calendar.day_name)[weekdayIndex]

def getWeekdayIndexByName(weekdayName):
    weekday_names = list(calendar.day_name)
    index = 0
    for weekday_name in weekday_names:
        if weekdayName.upper() == weekday_name.upper():
            return index
        index = index + 1