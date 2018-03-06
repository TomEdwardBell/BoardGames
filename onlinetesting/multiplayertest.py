from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials
import datetime, sys
from PyQt5 import QtWidgets, QtCore

class Master:
    def __init__(self):
        self.server = Server()
        id = 0
        maxid = (len(self.server.users.col_values(1)))

        while id >= maxid:
            id +=1
            print(self.server.users.row_values(id))


        self.user = User(self.server)


class Server:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_access.json', scope)
        client = authorize(creds)

        self.users = client.open("onlinetest").worksheet("users")

    def appenduser(self, username):
        usercount = self.users.row_count -1
        print(self.users.row_count)
        date = datetime.date.today()
        time = datetime.datetime.now().time()
        row = [usercount + 1,username,0,date,time]
        self.users.insert_row(row, usercount+2)
        yeet = CharacterCreation()


class Player:
    def __init__(self):
        self.username = ""
        self.score = 0
        self.id = 0

    def ppinfo(self):
        print(" __________________")
        print("|Username|",self.username)
        print("|ID      |",self.id)
        print("|Score   |",self.score)


class User(Player):
    def __init__(self, server):
        super(User, self).__init__()
        self.username = input("What is your username? ")

        server.appenduser(self.username)


class CharacterCreation(QtWidgets.QMainWindow):
    def __init__(self):
        super(CharacterCreation, self).__init__()
        self.show()
        print("fsdjkjvj")

    def lol(selfs):
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    game = Master()
    app.exec_()

if __name__ == '__main__':
    main()
