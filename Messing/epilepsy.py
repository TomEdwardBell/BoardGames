from PyQt5 import QtWidgets, QtTest, QtGui
import sys
import random


class Coord:
    def __init__(self, game):
        self.btn = QtWidgets.QPushButton(game)

    def setcolor(self, r,g,b):
        color = '#%02x%02x%02x' % (r, g ,b)
        self.btn.setStyleSheet("background-color:"+color)

class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.initUI()

    def initUI(self):
        boardx = 800
        boardy = 800
        border = 0
        xcount = 5
        ycount = 20
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
                #board[x, y].btn.setText(str(x) + "," + str(y))

        self.show()

        #making path
        path = []
        for x in range(xcount - 1):
            path.append([x,0])
        for y in range(ycount - 1):
            path.append([xcount - 1,y])
        for x in range(xcount - 1):
            path.append([(xcount - (x + 1)),ycount - 1])
        for y in range(ycount):
            path.append([0,(ycount - (y + 1))])

        count = 0
        colorstats = {"r": "full", "g": "empty", "b": "change"}
        while True:
            for i in path:
                count += 3


                x = i[0]
                y = i[1]


                colors = {}
                for color in colorstats:
                    if colorstats[color] == "full":
                        colors[color] = 255
                    if colorstats[color] == "empty":
                        colors[color] = 0
                    if colorstats[color] == "change":
                        colors[color] = count%256

                if count > 255:
                    if colorstats["r"] == "full":
                        colorstats["r"] = "change"
                        colorstats["g"] = "empty"
                        colorstats["b"] = "full"
                    elif colorstats["g"] == "full":
                        colorstats["g"] = "change"
                        colorstats["b"] = "empty"
                        colorstats["r"] = "full"
                    elif colorstats["b"] == "full":
                        colorstats["b"] = "change"
                        colorstats["r"] = "empty"
                        colorstats["g"] = "full"
                    count = 0



                r = colors["r"]
                g = colors["g"]
                b = colors["b"]
                board[x, y].setcolor(r, g, b)
                QtGui.QGuiApplication.processEvents()


    def printcoord(self, coord):
        print(coord.coordinates)

def main():
    app = QtWidgets.QApplication(sys.argv)
    game = Grid()
    game.show()
    app.exec_()


if __name__ == '__main__':
    main()
