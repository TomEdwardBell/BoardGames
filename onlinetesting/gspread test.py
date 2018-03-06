import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Server:
    def __init__(self, servernumber):
        servername = "Sever" + str(servernumber)
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_access.json', scope)
        client = gspread.authorize(creds)

        self.sheet = client.open("KAConline").worksheet(servername)


for x in range(3):
    for y in range(3):
        print(sheet.cell(x+1,y+1).value,end= "")
    print("")

