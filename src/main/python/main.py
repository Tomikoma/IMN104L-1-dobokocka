from fbs_runtime.application_context.PyQt5 import ApplicationContext
from DiceValueRecognizer.python.app import MainWindow
import sys


if __name__ == '__main__':
    appctxt = ApplicationContext()
    startWindow = MainWindow()
    startWindow.show()
    sys.exit(appctxt.app.exec_())
