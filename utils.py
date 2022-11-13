import sys, os, calendar

from PyQt6 import uic

def loadUi(relative_filename, parentWidget):

    ui_filename = ""
    if isRunFromPyInstallerExeWithOneFileOption():
        ui_filename = os.path.join(sys._MEIPASS, relative_filename)
    else:
        ui_filename = relative_filename

    return uic.loadUi(ui_filename, parentWidget)

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