import gspread, sys
from PyQt5 import QtWidgets, QtTest
from oauth2client.service_account import ServiceAccountCredentials
import random



class Server:
    def __init__(self):
        servername = "null"
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_access.json', scope)
        client = gspread.authorize(creds)
        print("jljf")
        self.sheet = client.open("KAConline").worksheet(servername)
        self.board = {}
        print(self.board)

    def changeserver(self,severnumber):


    def checkboard(self):
        for x in range(3):
            for y in range(3):
                pass
                #self.sheet

class Coord:
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
        self.server = Server()

        self.initUI()


    def initUI(self):
        boardx = 650
        boardy = 650
        border = 0
        xcount = 3
        ycount = 3

        self.resize(boardx + border * (xcount + 1), boardy + border * (xcount + 1))
        for x in range(xcount):
            for y in range(ycount):
                self.server.board[x, y] = Coord(self)
                self.server.board[x, y].coordinates = [x, y]

                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x*xpercoord + (x+1)*border)
                yloc = (y*ypercoord + (y+1)*border)
                self.server.board[x, y].btn.move(xloc, yloc)
                self.server.board[x, y].btn.resize(boardx/xcount, boardy/ycount)


        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y].btn.clicked.connect(lambda state, c=(x, y): self.btnclicked(c))

    def btnclicked(self, coords):
        pass

    def loadboard(self):
        for x in range(3):
            for y in range(3):
                newvalue = self.server

                self.board[x ,y].setValue(newvalue)


def main():
    app = QtWidgets.QApplication(sys.argv)
    game = Grid()
    game.show()
    app.exec_()


if __name__ == '__main__':
    main()