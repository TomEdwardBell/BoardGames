from gspread import authorize
import sys
from PyQt5 import QtWidgets, QtTest, QtCore, QtGui
from oauth2client.service_account import ServiceAccountCredentials
import random
import time


class Menu(QtWidgets.QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        self.widgets = {}
        self.initUI()
        self.show()

    def initUI(self):
        self.resize(512, 256)

        self.widgets["title_lbl"] = QtWidgets.QLabel(self)
        self.widgets["title_lbl"].setText("Noughts and Crosses!")
        self.widgets["title_lbl"].resize(512,60)
        self.widgets["title_lbl"].setStyleSheet("font-size: 50px")
        self.widgets["title_lbl"].setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["subtitle_lbl"] = QtWidgets.QLabel(self)
        self.widgets["subtitle_lbl"].setText("Online")
        self.widgets["subtitle_lbl"].move(0,60)
        self.widgets["subtitle_lbl"].resize(512, 40)
        self.widgets["subtitle_lbl"].setStyleSheet("font-size: 35px; font-style: italic")
        self.widgets["subtitle_lbl"].setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["start_btn"] = QtWidgets.QPushButton(self)
        self.widgets["start_btn"].move(0,128)
        self.widgets["start_btn"].resize(256,128)
        self.widgets["start_btn"].setText("Start")
        #self.widgets["start_btn"].clicked.connect(lambda:self.widgets["title_lbl"].setText("Loading"))

        self.widgets["start_btn"].clicked.connect(self.gameload)

        self.widgets["quit_btn"] = QtWidgets.QPushButton(self)
        self.widgets["quit_btn"].move(256, 128)
        self.widgets["quit_btn"].resize(256, 128)
        self.widgets["quit_btn"].setText("Quit")
        self.widgets["quit_btn"].clicked.connect(sys.exit)

    def gameload(self):
        self.hide()
        selection = GameSelect()
        player = selection.info()
        load = Loading()
        game = Grid(player)
        game.show()
        load.hide()


class GameSelect(QtWidgets.QMainWindow):
    def __init__(self):
        super(GameSelect, self).__init__()
        self.widgets = {}

    def info(self):
        player = self.Player()
        print(self.Player.name)
        return(player)


class Player:
    def __init__(self):
        self.username = ""
        self.type = "" #other or user
        self.

class Loading(QtWidgets.QMainWindow):
    def __init__(self):
        super(Loading, self).__init__()
        self.widgets = {}
        self.widgets["title_lbl"] = QtWidgets.QLabel(self)
        self.widgets["title_lbl"].resize(512, 60)
        self.widgets["title_lbl"].setStyleSheet("font-size: 50px")
        self.widgets["title_lbl"].setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["subtitle_lbl"] = QtWidgets.QLabel(self)
        self.widgets["subtitle_lbl"].move(0, 60)
        self.widgets["subtitle_lbl"].resize(512, 40)
        self.widgets["subtitle_lbl"].setStyleSheet("font-size: 35px; font-style: italic")
        self.widgets["subtitle_lbl"].setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["title_lbl"].setText("Loading")
        self.widgets["subtitle_lbl"].setText("Please wait")
        self.resize(512, 128)
        self.show()
        QtGui.QGuiApplication.processEvents()

class Grid(QtWidgets.QMainWindow):
    def __init__(self, player):
        super(Grid, self).__init__()
        self.hide()

        self.server = Server()
        self.widgets = {}
        self.initUI()

    def initUI(self):
        boardx = 650
        boardy = 650
        header = 60
        border = 0
        xcount = 3
        ycount = 3

        self.widgets["servernamelbl"] = QtWidgets.QLabel(self)
        self.widgets["servernamelbl"].setText(self.server.getvalue(4, 1))
        self.widgets["servernamelbl"].resize(90, 30)
        self.widgets["servernamelbl"].move(0, 0)


        self.widgets["changeserverln"] = QtWidgets.QLineEdit(self)
        self.widgets["changeserverln"].move(0, 30)
        self.widgets["changeserverln"].resize(90, 30)

        self.widgets["changeserverbtn"] = QtWidgets.QPushButton(self)
        self.widgets["changeserverbtn"].move(90, 30)
        self.widgets["changeserverbtn"].resize(100, 30)
        self.widgets["changeserverbtn"].setText("Change Server")

        self.resize(boardx + border * (xcount + 1), boardy + border * (xcount + 1) + header)


        self.makeboard(xcount, ycount, border, header, boardx, boardy)


    def makeboard(self, xcount, ycount, border, header, boardx, boardy):
        for x in range(xcount):
            for y in range(ycount):
                self.server.board[x, y] = Coord(self)
                self.server.board[x, y].coordinates = [x, y]

                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x * xpercoord + (x + 1) * border)
                yloc = (y * ypercoord + (y + 1) * border + header)
                self.server.board[x, y].btn.move(xloc, yloc)
                self.server.board[x, y].btn.resize(boardx / xcount, boardy / ycount)

                self.server.board[x, y].value = self.server.getvalue(x, y)

        for x in range(xcount):
            for y in range(ycount):
                self.server.board[x, y].btn.clicked.connect(lambda state, c=(x, y): self.btnclicked(c))

    def btnclicked(self, coords):
        newvalue = (int(self.server.getvalue(coords[0], coords[1]))) + 1
        x = coords[0]
        y = coords[1]
        self.server.newvalue(x, y, newvalue)

    def loadboard(self):
        for x in range(3):
            for y in range(3):
                newvalue = self.server

                self.board[x, y].setValue(newvalue)


class Server:
    def __init__(self):
        servername = "test"
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_access.json', scope)
        client = authorize(creds)

        self.sheet = client.open("NAConline").worksheet(servername)
        self.board = {}
        print(self.board)

    def changeserver(self, severname):
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_access.json', scope)
        client = authorize(creds)
        self.sheet = client.open("NAConline").worksheet(severname)

    def checkboard(self):
        for x in range(3):
            for y in range(3):
                pass
                # self.sheet

    def getvalue(self, x, y):
        value = self.sheet.cell((y + 1), (x + 1)).value

        return (value)

    def newvalue(self, x, y, change):
        self.sheet.update_cell((y + 1), (x + 1), str(change))
        self.board[x, y].btn.setText(str(change))


class Coord:
    def __init__(self, game):
        self.btn = QtWidgets.QPushButton(game)

    def setcolor(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)
        self.btn.setStyleSheet("background-color:" + color)

    def setvalue(self, newtext):
        self.btn.setText(newtext)


def main():
    app = QtWidgets.QApplication(sys.argv)
    menu = Menu()
    app.exec_()


if __name__ == '__main__':
    main()
