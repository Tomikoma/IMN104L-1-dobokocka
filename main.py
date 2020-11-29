from DiceValueRecognizer.python.app import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication([])
    startWindow = MainWindow()
    startWindow.show()
    app.exit(app.exec_())
