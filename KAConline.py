from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import time


class Coord():
    def __init__(self, game):
        self.btn = QtWidgets.QPushButton(game)
        self.value = " "


    def setcolor(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)
        self.btn.setStyleSheet("background-color:" + color)

    def setValue(self, tochangeto):
        self.value = tochangeto
        self.btn.setText(self.value)
        self.btn.setStyleSheet("font-size: 50pt")


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.currentturn = "O"  # "X" or "O"
        self.board = {}
        self.won = False
        self.initUI()

    def initUI(self):
        boardx = 700
        boardy = 700
        border = 3
        xcount = 3
        ycount = 3

        self.resize(boardx + border * (xcount + 1), boardy + border * (xcount + 1))
        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y] = Coord(self)
                self.board[x, y].coordinates = [x, y]
                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x*xpercoord + (x+1)*border)
                yloc = (y*ypercoord + (y+1)*border)
                self.board[x, y].btn.move(xloc, yloc)
                self.board[x, y].btn.resize(boardx/xcount, boardy/ycount)

        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y].btn.clicked.connect(lambda state, c=(x, y): self.doturn(c))

    def doturn(self, coordnumbers):
        if self.board[coordnumbers].value == " " and self.won == False:
            if self.currentturn == "O":
                nextturn = "X"
            if self.currentturn == "X":
                nextturn = "O"

            self.currentturn = nextturn
            self.board[(coordnumbers[0],coordnumbers[1])].setValue(self.currentturn)
            self.checkboard()

    def checkboard(self):
        possiblewins = [
            [[0, 0], [0, 1], [0, 2]],
            [[1, 0], [1, 1], [1, 2]],
            [[2, 0], [2, 1], [2, 2]],

            [[0, 0], [1, 0], [2, 0]],
            [[0, 1], [1, 1], [2, 1]],
            [[0, 2], [1, 2], [2, 2]],

            [[0, 0], [1, 1], [2, 2]],
            [[0, 2], [1, 1], [2, 0]]
        ]
        for player in ["O", "X"]:
            for winningboard in possiblewins:
                wonyet = True
                for coord in winningboard:
                    x = coord[0]
                    y = coord[1]
                    if not (self.board[x, y].value == player) or self.board[x, y].value == "":
                        wonyet = False

                if wonyet:
                    winner = player
                    self.win(winner, winningboard)

    def win(self,winner, winningboard):
        self.won = True
        for i in winningboard:
            x = i[0]
            y = i[1]
            self.board[x, y].btn.setStyleSheet("background-color: #33DD36; font-size: 60pt;")



    def printcoord(self, coord):
        print(coord.coordinates)

def main():
    app = QtWidgets.QApplication(sys.argv)
    game = Grid()
    game.show()
    app.exec_()


if __name__ == '__main__':
    main()