from sys import argv, exit, exc_info
from PyQt5 import QtWidgets, QtCore, QtGui
import socket
from threading import Thread
import random

class MainGame():
    def __init__(self):
        self.menu = Menu()
        self.gametype = ""

    def game_as_client(self):
        self.gametype = "client"
        self.username = self.menu.username

    def game_as_server(self):
        self.gametype = "server"
        self.servername = "nac-"+random.randint(1000,9999)


class Menu():
    def __init__(self):
        self.done = False
        self.username = ""
        self.welcome_screen = self.WelcomeScreen(self)

    class WelcomeScreen(QtWidgets.QMainWindow):
        def __init__(self,parent):
            super(Menu.WelcomeScreen, self).__init__()
            self.widgets = {}
            self.init_ui(parent)


        def init_ui(self, parent):
            self.resize(300, 300)

            self.widgets["title_lbl"] = QtWidgets.QLabel(self)
            self.widgets["title_lbl"].setText("Game")
            self.widgets["title_lbl"].setStyleSheet("font-size: 30pt")
            self.widgets["title_lbl"].setAlignment(QtCore.Qt.AlignCenter)
            self.widgets["title_lbl"].resize(300, 150)
            self.widgets["title_lbl"].move(0, 0)

            self.widgets["ok_btn"] = QtWidgets.QPushButton(self)
            self.widgets["ok_btn"].clicked.connect(lambda x: self.select_game(parent))
            self.widgets["ok_btn"].setText("Play")
            self.widgets["ok_btn"].setStyleSheet("font-size: 30pt")
            self.widgets["ok_btn"].resize(300, 150)
            self.widgets["ok_btn"].move(0, 150)


            self.show()

        def select_game(self,parent):
            parent.select_game = parent.SelectGame(parent)

    class UserNameSelect(QtWidgets.QMainWindow):
        def __init__(self, parent):
            super(Menu.UserNameSelect, self).__init__()
            self.widgets = {}
            self.init_ui(parent)
            self.show()

        def init_ui(self,parent):
            self.resize(256, 128)

            self.widgets["username_lbl"] = QtWidgets.QLabel(self)
            self.widgets["username_lbl"].setText("UserName")
            self.widgets["username_lbl"].setStyleSheet("font-size: 20pt;")
            self.widgets["username_lbl"].resize(256, 32)

            self.widgets["username_ln"] = QtWidgets.QLineEdit(self)
            self.widgets["username_ln"].resize(256, 32)
            self.widgets["username_ln"].move(0, 64)

            self.widgets["ok_btn"] = QtWidgets.QPushButton(self)
            self.widgets["ok_btn"].resize(128, 32)
            self.widgets["ok_btn"].move(0, 96)
            self.widgets["ok_btn"].setText("Okay")
            self.widgets["ok_btn"].clicked.connect(lambda x: self.username_done(parent))

        def username_done(self, parent):
            print("E")
            possible_username = self.widgets["username_ln"].text()
            valid = False
            while not valid:
                valid = True
            parent.username = possible_username

            self.open_select_game(parent)

        def open_select_game(self,parent):
            self.hide()
            parent.select_game = parent.SelectGame(parent)

    class SelectGame(QtWidgets.QMainWindow):
        def __init__(self, parent):
            super(Menu.SelectGame, self).__init__()
            self.resize(300, 300)
            self.widgets = {}
            parent.username = "user"+str(random.randint(1000,9999))
            self.start_game(parent)

        def start_game(self, parent):
            self.resize(200, 100)

            self.widgets["clientstart"] = QtWidgets.QPushButton(self)
            self.widgets["clientstart"].resize(100, 100)
            self.widgets["clientstart"].move(0, 0)
            self.widgets["clientstart"].setText("Start As \n Client")
            self.widgets["clientstart"].clicked.connect(lambda: self.start_client(parent, self.username))

            self.widgets["serverstart"] = QtWidgets.QPushButton(self)
            self.widgets["serverstart"].resize(100, 100)
            self.widgets["serverstart"].move(100, 0)
            self.widgets["serverstart"].setText("Start As \n Host")
            self.widgets["serverstart"].clicked.connect(lambda: self.start_server(parent, self.username))


            self.show()

        def start_client(self,parent,username):
            parent.start_client()

        def start_server(self,parent,username):
            pass

class BoardUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(BoardUi, self).__init__()
        self.widgets = {}
        self.coords = {}
        self.dimensions = [900, 900]

        self.init_ui()

    def init_ui(self):
        self.resize(self.dimensions[0], self.dimensions[1])
        self.make_board(3,3)

    def make_board(self,xcount,ycount):
        xpercoord = (self.dimensions[0] / xcount)
        ypercoord = (self.dimensions[1] / ycount)
        for x in range(xcount):
            for y in range(ycount):
                self.coords[x, y] = Coord(self)
                self.coords[x, y].coordinates = [x, y]

                xloc = (x * xpercoord)
                yloc = (y * ypercoord)
                self.coords[x, y].move(xloc, yloc)
                self.coords[x, y].resize(self.dimensions[0] / xcount, self.dimensions[1] / ycount)

                self.coords[x, y].set_text("...")

        self.show()


class Server:  # Totally not stolen code...
    def __init__(self):
        print("Server created")
        self.start_server()

    def processing(self,toprocess):
        print("Processing "+toprocess)
        # Should be like s22X
        # Will set the coordinate 2,2 to X
        return (toprocess)

    def client_thread(self, conn, ip, port):
        # the input is in bytes, so decode it
        clientinput_bytes = conn.recv(4096)

        # decode input and strip the end of line
        clientinput_string = clientinput_bytes.decode("utf8").rstrip()

        res = self.processing(clientinput_string)
        print("Result of processing {} is: {}".format(clientinput_string, res))

        vysl = res.encode("utf8")  # encode the result string
        conn.sendall(vysl)  # send it to client
        # conn.close()  # close connection
        print('Connection ' + ip + ':' + port + " ended")

    def start_server(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this is for easy starting/killing the app
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket created')

        try:
            soc.bind(("127.0.0.1", 12345))
            print('Socket bind complete')
        except socket.error as msg:
            print('Bind failed. Error : ' + str(exc_info()))
            exit()

        soc.listen(10)
        print('Socket now listening')
        accepting = True
        while accepting:
            conn, addr = soc.accept()
            ip, port = str(addr[0]), str(addr[1])
            print('Accepting connection from ' + ip + ':' + port)

            Thread(target=self.client_thread, args=(conn, ip, port)).start()

        soc.close()


class Client:
    def __init__(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(("127.0.0.1", 12345))

        clients_input = input("Send to Server")
        soc.send(clients_input.encode("utf8"))

        result_bytes = soc.recv(4096)
        result_string = result_bytes.decode("utf8")

        print("Result from server is {}".format(result_string))

class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.coordinates = []
        # Adding custom attributes to QtWidgets.QPushButton

    def set_text(self,text):
        self.setText(text)
        chrcount = str(int(200 / len(text)))
        print(chrcount)
        self.setStyleSheet("font-size: "+chrcount+"pt ;")
        # This will set the text, and resize it appropriatly

def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()
