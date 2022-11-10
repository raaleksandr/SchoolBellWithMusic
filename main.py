import sys

from controller import SchoolBellController

if __name__ == '__main__':
    controller = SchoolBellController(sys.argv)
    controller.run_application()