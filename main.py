import sys

from controller import SchoolBellController

if __name__ == '__main__':
    controller = SchoolBellController()
    controller.run_application(sys.argv)