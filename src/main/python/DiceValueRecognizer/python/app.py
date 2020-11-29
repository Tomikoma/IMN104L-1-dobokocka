from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, QFileDialog, QLabel, QApplication
from PyQt5.QtGui import QImage, QPixmap
from imutils import resize
from hough.hough import getDiceValue
from cnn.cnn import predict_cnn
import os

import cv2

def makeQImageFromOpenCVImage(image):
    height, width, channel = image.shape
    bytesPerLine = 3 * width
    return QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DiceValueRecognizer")
        self.centralWidget = QWidget()
        self.layout = QVBoxLayout(self.centralWidget)
        self.imageFrameWidget = QLabel()
        self.layout.addWidget(self.imageFrameWidget)
        self.setCentralWidget(self.centralWidget)

        toolBar =self.addToolBar("Fájl")
        openImage = QAction("Megnyitás",self)
        self.recognizeValueWithNeuralNetwork = QAction("Neuronháló", self)
        self.recognizeValueWithNeuralNetwork.setEnabled(False)
        self.recognizeValueWithHoughCircles = QAction("Hough körök", self)
        self.recognizeValueWithHoughCircles.setEnabled(False)

        toolBar.addAction(openImage)
        toolBar.addAction(self.recognizeValueWithNeuralNetwork)
        toolBar.addAction(self.recognizeValueWithHoughCircles)
        toolBar.actionTriggered[QAction].connect(self.toolButtonPressed)
        self.imagePath = None
        self.dialog = None

    def toolButtonPressed(self, action):
        if action.text() == "Megnyitás" and self.openFileNameDialog():
            print("megnyitás")
        if action.text() == "Neuronháló":
            print("Neuronháló")
            value = predict_cnn(self.imagePath)
            print("Value:", value)
            self.dialog = DialogWindow(value, self)
            self.dialog.show()
        if action.text() == "Hough körök":
            print("Hough körök")
            value = getDiceValue(self.imagePath)
            print("Value:", value)
            self.dialog = DialogWindow(value, self)
            self.dialog.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "All Images (*.jpg *.png *.jpeg);;JPG Files (*.jpg)", options=options)
        if fileName:
            self.imagePath = fileName
            self.showImage(cv2.imread(fileName))
            self.recognizeValueWithHoughCircles.setEnabled(True)
            self.recognizeValueWithNeuralNetwork.setEnabled(True)
            #self.setNoiseAction.setEnabled(True)
        return fileName != ""


    def showImage(self, openCVImage):
        image = makeQImageFromOpenCVImage(resize(openCVImage,500,500))
        self.imageFrameWidget.setPixmap(QPixmap.fromImage(image))


class DialogWindow(QMainWindow):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dobókocka értéke")
        self.diceValue = QLabel("Érték: " + str(value))
        layout = QVBoxLayout()
        layout.addWidget(self.diceValue)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


def benchmark(path: str, debug=False):
    n = 0
    hough = 0
    nn = 0
    for dir in os.listdir(path):
        realValue = int(dir.split("_")[1])

        for filename in os.listdir(path + "/" + dir) :
            if "im" in filename:
                continue
            # predictedValue = getDiceValue(path + "/" + dir + "/" + filename, debug)
            n += 1
            if predict_cnn(path + "/" + dir + "/" + filename) == realValue:
                nn += 1
            # print("Érték:",realValue,"|Felismert:",predictedValue, ("JÓ" if predictedValue == realValue else ""))
            if getDiceValue(path + "/" + dir + "/" + filename) == realValue:
                hough += 1

    print(hough, "/", n, "=", hough/n)
    print(nn, "/", n, "=", nn/n)
