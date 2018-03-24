from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import random


class MainGame:
    def __init__(self):
        print("Game Initialising...")
        self.clicks = 0
        self.mine_count = 9
        self.dimensions = (10, 10)
        self.ui = Grid(self.dimensions)
        self.set_mines()
        self.set_slots()
        self.mouse_mode = "normal"
        self.ui.show()

    def set_mines(self):
        for i in range(self.mine_count):
            mine_placed = False
            while not mine_placed:
                mine_placed = True
                mine_x = random.randint(0, self.dimensions[0] -1)
                mine_y = random.randint(0, self.dimensions[1] -1)

            if self.ui.board[mine_x, mine_y].hidden_value == "x":
                mine_placed = False

            self.ui.board[mine_x, mine_y].set_value("x")

    def set_slots(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.ui.board[x, y].clicked.connect(lambda state, c=(x, y): self.clicked(c))
        self.ui.widgets["flag_btn"].clicked.connect(self.flag_switch)

    def clicked(self, coords):
        x = coords[0]
        y = coords[1]
        if self.mouse_mode == "flag":
            if self.ui.board[x, y].state == "hidden":
                self.ui.board[x, y].set_value("F")

        elif self.mouse_mode == "normal":

            if self.ui.board[x, y].state == "hidden":
                self.ui.board[x, y].state = "shown"
            if self.ui.board[x, y].hidden_value == "x":
                self.game_over()
            else:
                minecount = self.get_minecount(coords)
                self.ui.board[x, y].set_value(minecount)
                if minecount == 0:  # The thing where if you click one of "0" it also removes the other nearby 0s
                    for localcoord in self.get_locals((x, y)): # Gets local coords
                        loc_x = localcoord[0]
                        loc_y = localcoord[1]
                        if self.ui.board[loc_x, loc_y].state == "hidden": # If they've not been clicked
                            self.clicked((localcoord[0], localcoord[1]))  # Oh sorry, is that recursion
                            # HELL YEAH IT IS!!!
                            # No but that command basically will click the nearby coord for you.

    def flag_switch(self):
        if self.mouse_mode == "normal":
            self.mouse_mode = "flag"
            self.ui.widgets["flag_lbl"].setText("Current Mode: Flag")
        elif self.mouse_mode == "flag":
            self.mouse_mode = "normal"
            self.ui.widgets["flag_lbl"].setText("Current Mode: Normal")

    def get_locals(self, coords):
        localcoords = []
        relative_locals = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

        for i in relative_locals:
            rel_x = i[0]
            rel_y = i[1]
            loc_x = coords[0] + rel_x
            loc_y = coords[1] + rel_y
            if -1 not in [loc_x, loc_y] and loc_x < self.dimensions[0] and loc_y < self.dimensions[1]:
                localcoords.append([loc_x, loc_y])
        return(localcoords)

    def get_minecount(self, coords):
        localcoords = self.get_locals(coords)

        minecount = 0

        for coord in localcoords:
            if self.ui.board[coord[0], coord[1]].hidden_value == "x":
                minecount += 1

        return(minecount)

    def checkwon(self):
        pass

    def game_over(self):
        print("DEAD")
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.ui.board[x, y].setStyleSheet("background-color: #FF0000; font-size: 50pt")


class Grid(QtWidgets.QMainWindow):
    def __init__(self, dimensions):
        super(Grid, self).__init__()
        self.dimensions = dimensions
        self.board = {}
        self.widgets = {}
        self.init_ui()

    def init_ui(self):
        boardx = 512
        boardy = 512
        margintop = 60
        borderx = 0
        bordery = 0
        xcount = self.dimensions[0]
        ycount = self.dimensions[1]

        self.widgets["flag_btn"] = QtWidgets.QPushButton(self)
        self.widgets["flag_btn"].setText("Change Mouse Mode")
        self.widgets["flag_btn"].resize(150, 40)

        self.widgets["flag_lbl"] = QtWidgets.QLabel(self)
        self.widgets["flag_lbl"].setText("Current Mode: Normal")
        self.widgets["flag_lbl"].resize(150, 20)
        self.widgets["flag_lbl"].move(0, 40)

        self.resize((boardx + borderx * (xcount + 1)), (boardy + bordery * (ycount + 1)) + margintop)
        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y] = Coord(self)
                self.board[x, y].coordinates = [x, y]
                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x*xpercoord + (x+1)*borderx)
                yloc = (y*ypercoord + (y+1)*bordery + margintop)
                self.board[x, y].move(xloc, yloc)
                self.board[x, y].resize(boardx/xcount, boardy/ycount)

    def print_coord(self, coord):
        print(coord.coordinates)

    def win(self):
        for x in range(10):
            for y in range(10):
                toerase = ["•", "O", " "]
                if self.board[x, y].hidden_value in toerase:
                    self.board[x, y].set_value(" ")
                    self.board[x, y].setStyleSheet('''
                    font-size: 35pt;
                    background-color: #22FF11;
                    ''')
                else:
                    self.board[x, y].setStyleSheet('''
                    background-color: #FFFFFF;
                    font-size: 35pt;
                    ''')


class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.hidden_value = " "
        self.shown_value = " "
        self.setStyleSheet("font-size: 30pt")
        self.color_numbers = {
            0: "#333333",
            1: "#DD1111",
            2: "#55EE11",
            3: "#11EE22",
            4: "#1155FF",
            5: "#EE00EE",
            6: "#FF0000",
            7: "#EE6600",
            8: "#6611AA"
        }
        self.state = "hidden" #hidden or shown, depends on whether it's been clicked

    def set_color(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)
        self.setStyleSheet("background-color:" + color)

    def set_value(self, tochangeto):
        if tochangeto == "x":
            self.hidden_value = tochangeto
            self.shown_value = " "
        elif tochangeto == "F":
            self.shown_value = "F"
            self.setStyleSheet("font-size: 40pt; color: #551111")
        elif tochangeto in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            if self.state == "hidden":
                self.shown_value = " "

            if self.state == "shown":
                fontcolor = self.color_numbers[tochangeto]
                self.shown_value = tochangeto
                self.setStyleSheet("font-size: 30pt; color: " + fontcolor)

            self.hidden_value = tochangeto

        self.setText(str(self.shown_value))



def main():
    app = QtWidgets.QApplication(sys.argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()
