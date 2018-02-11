from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import sys
import random
from functools import partial


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.initUI()
        self.tracker = QtWidgets.QPushButton(self)
        self.tracker.resize(0,0)

    def initUI(self):
        boardx = 800
        boardy = 800

        self.resize(boardx, boardy)

        startbtn = QtWidgets.QPushButton(self)
        startbtn.move(10, 100)
        startbtn.move(10, 10)
        startbtn.clicked.connect(self.starttrack)

    def starttrack(self):
        pass
        print("KJL")
        while True:
            QtTest.QTest.qWait(0)
            self.tracker.resize(100, 100)
            QtGui.QCursor.setPos(random.randint(0,1000),random.randint(0,1000))
            self.tracker.move(0,0)
            print("jfdkl")

def main():
    app = QtWidgets.QApplication(sys.argv)
    game = Grid()
    game.show()
    app.exec_()


if __name__ == '__main__':
    main()
