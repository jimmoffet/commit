from bs4 import BeautifulSoup
import requests
import requests.exceptions
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fbcreds import app_id, app_secret

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
    longtoken = resp['access_token']
    print(resp['access_token'])
    #{'access_token': 'EAACyc2hNZCsABAA7t8mRlg3ADekZBTHZA1fw5misTnwczPZBftobR9pTSXrlih9zYi775vaPdjgZABpHYehX927sNZCBsOwatTW5rZANIZCCucsK52oZCiATT9r6Wl3sTTaMAzObXgh75Ft3lbr7jLtXemqgt0bZCp9ruiD2ZAzyksVSgZDZD', 'token_type': 'bearer', 'expires_in': 5179108}

    return longtoken

def getUserFromRef(refcode):
    #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    name = getRow(refcode);
    #name = sheetList[row][1]
    return name

def getRow(uid):

    rlen = len(sheetList)
    clen = len(sheetList[0])
    peeps = {}
    cnt = 0
    namerow = 0
    new = True

    for row in range(rlen):
        if row == 0:
            continue
        cnt += 1
        zerocell = sheetList[row][0]
        #print "uid zerocell",uid,zerocell
        if str(uid) == str(zerocell):
            #print "uid zerocell",uid,zerocell
            new = False
            #print "new is ",new
            break
        
    if(new):
        row = cnt+2
        #sheet.update_cell(row, 2, "unknown user") # pos message
        name = "Team COMM!T"
    else:
        row = cnt
        name = sheetList[row][1]

    return name

def writeMessageToDB(message):
    # use creds to create a client to interact with the Google Drive API

    row = 2
    #row = getRow(uid)

    sheet.update_cell(row, 4, message) # pos message

    return message

def writeMessageToDB2(message):
    # use creds to create a client to interact with the Google Drive API

    row = 2
    #row = getRow(uid)

    sheet.update_cell(row, 5, message) # pos message

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



def writeAll(json_dict):
    uid = json_dict['uid']
    longToken = json_dict['longToken']
    friends = ''
    timeStamp = datetime.datetime.now()
    message1 = ""
    message2 = ""

    row = getRow(uid)
    sheet.update_cell(row, 2, timeStamp)
    sheet.update_cell(row, 3, longToken)
    sheet.update_cell(row, 8, friends)
    sheet.update_cell(row, 4, message1)
    sheet.update_cell(row, 5, message2)

    return 'writeAll succeeded'


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



