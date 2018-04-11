from PyQt5 import QtWidgets, QtGui, QtCore
from sys import argv
import datetime
import random


class MainGame:
    def __init__(self):
        self.ui = Ui(self)

        self.snakes = []
        self.food_pos = (0, 0)
        self.direction = (0, 0)
        self.timer_available = True
        self.del_last_piece = True
        self.ui.init_ui()
        self.ui.show()

        self.add_snake_piece((1, 1))
        self.main_loop()

    def food_eaten(self):
        self.del_last_piece = False

    def change_direction(self, change):
        self.direction = change
        self.tick()

    def place_snake(self):
        pass

    def add_snake_piece(self, coords):
        x, y = coords
        snake_piece = SnakePiece(self.ui, coords, self.ui.scale)
        snake_piece.show()

        self.snakes = [snake_piece] + self.snakes

    def main_loop(self):
        dead = False
        tick_count = 0
        while not dead:
            tick_count += 1
            if self.timer_available:
                self.timer_available = False
                timer = QtCore.QTimer()
                timer.timeout.connect(self.main_loop_timer_done)
                timer.start(0)
            QtGui.QGuiApplication.processEvents()

    def main_loop_timer_done(self):
        self.tick()
        self.timer_available = True


    def tick(self):

        newx = self.snakes[0].x + self.direction[0]
        newy = self.snakes[0].y + self.direction[1]

        if self.snakes[0].x + self.direction[0] > self.ui.grid_size[0]:
            newx = 0
        if self.snakes[0].y + self.direction[1] > self.ui.grid_size[1]:
            newy = 0
        if self.snakes[0].x + self.direction[0] < 0:
            newx = self.ui.grid_size[0]
        if self.snakes[0].y + self.direction[0] < 0:
            newy = self.ui.grid_size[0]

        self.add_snake_piece((newx, newy))

        if self.del_last_piece:
            self.snakes[-1].hide()
            print(len(self.snakes))
            del self.snakes[-1]
            print(len(self.snakes))
        else:
            self.del_last_piece = True

    def game_over(self):
        print("DEAD")


class Ui(QtWidgets.QMainWindow):
    def __init__(self, maingame):
        super(Ui, self).__init__()
        self.parent = maingame
        self.board = {}

        self.window_size = (600, 600)
        self.grid_size = (60, 60)

        self.margin = (5, 5, 5, 200) #Top margin, Bottom margin, Left Margin, Right Margin
        self.borders =(0, 0)
        self.piece_size = 0
        self.scale = 0

        self.widgets = self.Widgets()

    class Widgets:
        pass

    def init_ui(self):
        self.piece_size = min(self.window_size)
        boardx , boardy = self.window_size
        xcount , ycount = self.grid_size
        borderx, bordery = self.borders

        self.scale = (boardx / xcount, boardy / ycount)

        self.resize(boardx + self.margin[2] + self.margin[3], boardy + self.margin[0] + self.margin[1])

        self.widgets.arrow_up = QtWidgets.QPushButton(self)
        self.make_arrow_button(self.widgets.arrow_up, "up")
        self.widgets.arrow_dn = QtWidgets.QPushButton(self)
        self.make_arrow_button(self.widgets.arrow_dn, "dn")
        self.widgets.arrow_rt = QtWidgets.QPushButton(self)
        self.make_arrow_button(self.widgets.arrow_rt, "rt")
        self.widgets.arrow_lt = QtWidgets.QPushButton(self)
        self.make_arrow_button(self.widgets.arrow_lt, "lt")


    def make_arrow_button(self, arrow, direction):
        direction_chr = {"up": "⭡", "dn": "⭣", "rt": "⭢", "lt": "⭠"}
        direction_change = {"up": (0, -1), "dn": (0, 1), "rt": (1, 0), "lt": (-1, 0)}

        symbol = direction_chr[direction]
        arrow.setText(symbol)

        change = direction_change[direction]

        smallest_size = min([self.margin[3], self.height()])

        width = smallest_size / 3
        height = smallest_size / 3

        arrow.resize(width, height)
        xpos = self.width() - width*(-1 * change[0] + 2)
        ypos = 0 + height*(1 * change[1] + 1)
        arrow.move(xpos, ypos)
        arrow.setStyleSheet("font-size: 40px;")

        arrow.clicked.connect(lambda x: self.parent.change_direction(change))


class Food(QtWidgets.QPushButton):
    def __init__(self, ui, coords, scale):
        super(Food, self).__init__(ui)
        self.x, self.y = coords
        self.scalex, self.scaley = scale
        self.ui = ui
        self.goto(coords)
        self.setStyleSheet("background-color: ##eebb88")

    def goto(self, location):
        x, y = location
        self.move(x * self.scalex + self.ui.margin[2], y*self.scaley + self.ui.margin[0])
        self.resize(self.scalex, self.scaley)

class SnakePiece(QtWidgets.QPushButton):
    def __init__(self, ui, coords, scale):
        super(SnakePiece, self).__init__(ui)
        self.x, self.y = coords
        self.scalex, self.scaley = scale
        self.ui = ui
        self.goto(coords)
        self.setStyleSheet("background-color: #33EE33")

    def goto(self, location):
        x, y = location
        self.move(x * self.scalex + self.ui.margin[2], y*self.scaley + self.ui.margin[0])
        self.resize(self.scalex, self.scaley)



def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()
