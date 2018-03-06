from oauth2client.service_account import ServiceAccountCredentials
import datetime, sys
from PyQt5 import QtWidgets, QtCore


class creation(QtWidgets.QMainWindow):
    def __init__(self):
        super(creation, self).__init__()
        self.resize(400,400)
        self.show()
        

    def create(self):
        player = Player
        return(player)


class Player:
    def __init__(self):
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    game = creation()
    app.exec_()

if __name__ == '__main__':
    main()
