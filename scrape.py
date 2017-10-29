from bs4 import BeautifulSoup
import requests
import requests.exceptions
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import gspread
from oauth2client.service_account import ServiceAccountCredentials


app_id = "2024489881171070"
app_secret = "86339533a5793651f88deea4b2f254c0"

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("commitDB").sheet1
sheetList = sheet.get_all_values()

def ping(u):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    page = requests.get(u)
    return page

def extendToken(short_token):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # app_id = ''
    # app_secret = ''
    u = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&' + 'client_id=' + app_id + '&client_secret=' + app_secret + '&fb_exchange_token=' + short_token
    r = requests.get(u)
    resp = r.json()



    return resp  

def writeToDB(message):
    # use creds to create a client to interact with the Google Drive API
    
    sheet.update_cell(2, 4, message) # pos message

    return message

def writeUserToDB(message):
    # use creds to create a client to interact with the Google Drive API
    ### save longtoken to db along with uid and whatever else ###
    rlen = len(sheetList)
    clen = len(sheetList[0])
    peeps = {}

    for row in range(rlen):
        if row == 0:
            continue
        tmp = []
        for i in range(1,4):
            tmp.append(sheetList[row][i])
        peeps[sheetList[row][0]] = tmp

    cnt = 0
    new = True
    for key, val in peeps.items():
        cnt += 1
        if key == message:
            new = False
            break 
    #cnt+1 is current user, cnt+2 will write new line
    row = 0
    if(new):
        row = cnt+2
    else:
        row = cnt+1
    sheet.update_cell(row, 1, message) # pos message

    return 'success'


# get persistent layer as list of lists
def pLayer():
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("VoteBot App").sheet1
    # Extract and print all of the values
    #list_of_vals = sheet.get_all_values()
    return sheet


def people():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open("commitDB").sheet1
    sheetList = sheet.get_all_values()
    rlen = len(sheetList)
    clen = len(sheetList[0])
    peeps = {}
    for row in range(rlen):
        if row == 0:
            continue
        tmp = []
        for i in range(1,10):
            tmp.append(sheetList[row][i])
        peeps['+' + sheetList[row][0]] = tmp
    return peeps
        
# peoples = people()
# print(peoples)
# print('Done!')



