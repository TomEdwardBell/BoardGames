from PyQt5 import QtWidgets, QtTest
import sys
import random


class Coord:
    def __init__(self, game):
        self.btn = QtWidgets.QPushButton(game)

    def setcolor(self, color):
        if color == "rand":
            hexes = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
            color = "#"
            for q in range(6):
                color= color + random.choice(hexes)
        self.btn.setStyleSheet("background-color:"+color)

class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.initUI()

    def initUI(self):
        boardx = 800
        boardy = 800
        border = 0
        xcount = 10
        ycount = 10
        self.resize(boardx+border*(xcount+1), boardy+border*(ycount+1))
        board = {}

        for x in range(xcount):
            for y in range(ycount):
                board[x, y] = Coord(self)
                board[x, y].coordinates = [x,y]
                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x*xpercoord + (x+1)*border)
                yloc = (y*ypercoord + (y+1)*border)
                board[x, y].btn.move(xloc, yloc)
                board[x, y].btn.resize(boardx/xcount, boardy/ycount)
                board[x, y].setcolor("#FFFFFF")
                #board[x, y].btn.setText(str(x) + "," + str(y))

        self.show()
        while True:
            x = random.randint(0,(xcount-1))
            y = random.randint(0,(ycount-1))
            board[x, y].setcolor("#" + random.choice(["888888","858585"]))
            QtTest.QTest.qWait(0.001)

    def printcoord(self, coord):
        print(coord.coordinates)

def main():
    app = QtWidgets.QApplication(sys.argv)
    game = Grid()
    game.show()
    app.exec_()


if __name__ == '__main__':
    main()
