from DiceValueRecognizer.python.app import MainWindow
from PyQt5.QtWidgets import QApplication
from cnn.cnn import train_cnn


if __name__ == '__main__':
    # train_cnn()
    app = QApplication([])
    startWindow = MainWindow()
    startWindow.show()
    app.exit(app.exec_())