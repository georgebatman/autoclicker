from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pyautogui as clicker
import random
from ctypes import Structure, windll, c_uint, sizeof, byref
import threading
import time

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(256, 128)
        MainWindow.setMinimumSize(QtCore.QSize(10, 10))
        MainWindow.setMaximumSize(QtCore.QSize(256, 128))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonEnable = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEnable.setGeometry(QtCore.QRect(70, 10, 121, 23))
        self.pushButtonEnable.setObjectName("pushButtonEnable")
        # self.pushButtonEnable.setCheckable(True)
        # self.pushButtonEnable.setChecked(False)
        self.pushButtonEnable.clicked.connect(self.runCode) #link function
        self.pushButtonDisable = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDisable.setGeometry(QtCore.QRect(70, 50, 121, 23))
        self.pushButtonDisable.setObjectName("pushButtonDisable")
        # self.pushButtonDisable.setCheckable(True)
        # self.pushButtonDisable.setChecked(False)
        self.pushButtonDisable.clicked.connect(self.stopClicker) #link function
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 256, 20))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def runCode(self):
        global run
        run = True
        c = threading.Thread(target=self.startClicker, name='startClicker')
        c.daemon = True
        c.start()

    def startClicker(self):
        global run
        try:
            while run:
                windowSizeWidth, windowSizeHeight = clicker.size()
                cursorPositionX, cursorPositionY = clicker.position()
                idleFor = self.get_idle_duration()
                if idleFor > 5:
                    randomCursorPositionX, randomCursorPositionY = random.randrange(windowSizeWidth), random.randrange(windowSizeHeight)
                    clicker.moveTo(randomCursorPositionX, randomCursorPositionY)
                    clicker.moveTo(cursorPositionX, cursorPositionY)
                else:
                    continue
                time.sleep(10)
        except KeyboardInterrupt:
            pass            

    def stopClicker(self):
        global run
        run = False

    def get_idle_duration(self):
        lastInputInfo = LASTINPUTINFO()
        lastInputInfo.cbSize = sizeof(lastInputInfo)
        windll.user32.GetLastInputInfo(byref(lastInputInfo))
        millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
        return millis / 1000.0

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoClicker"))
        self.pushButtonEnable.setText(_translate("MainWindow", "Start AutoClicker"))
        self.pushButtonDisable.setText(_translate("MainWindow", "Stop AutoClicker"))

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def main():
    global run
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
