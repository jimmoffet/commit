from bs4 import BeautifulSoup
import requests
import requests.exceptions
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fbcreds import app_id, app_secret
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import datetime

# Find these values at https://twilio.com/user/account
account_sid = "AC3e1252b3f55741e9dfeb3fb4ef66d88e"
auth_token = "2e89e4f761bee93067348899cc5e6493"
client = Client(account_sid, auth_token)

# scope = ['https://spreadsheets.google.com/feeds']
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
# client = gspread.authorize(creds)
# sheet = client.open("commitDB").sheet1
# sheetList = sheet.get_all_values()

def ping(u):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    page = requests.get(u)
    return page

def extendToken(short_token):
    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # app_id = ''
    # app_secret = ''
    u = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&' + 'client_id=' + app_id + '&client_secret=' + app_secret + '&fb_exchange_token=' + short_token
    r = requests.get(u)
    print(r)
    resp = r.json()
    print(resp)
    longtoken = resp['access_token']
    print(resp['access_token'])
    #{'access_token': 'EAACyc2hNZCsABAA7t8mRlg3ADekZBTHZA1fw5misTnwczPZBftobR9pTSXrlih9zYi775vaPdjgZABpHYehX927sNZCBsOwatTW5rZANIZCCucsK52oZCiATT9r6Wl3sTTaMAzObXgh75Ft3lbr7jLtXemqgt0bZCp9ruiD2ZAzyksVSgZDZD', 'token_type': 'bearer', 'expires_in': 5179108}

    return longtoken

def sendSMS(from_num,refname,uid):
    ### get phone number

    cnt=1

    reminder = "COMM!Tbot says, You're committed! We'll let "+refname+" know when you check in at the polls tomorrow (or if you don't). We'll send you a few location-aware check-in reminders until you check in. Do for others what "+refname+" is doing for you with your COMM!T link: "+"http://www.commit.vote/r/"+

    from_num = '+'+from_num

    # now = datetime.datetime.now()
    # now = now.replace(second=0, microsecond=0)

    #test = datetime.datetime.strptime(subscriber[1],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=7)
    # print('Found +17733541500')
    # print(from_num)
    
    try:
        message = client.api.account.messages.create(to=from_num, from_="+16172497881", body=reminder)
    except Exception as e:
        print(e)
        return e
    else:
        print('send_sms sent "'+ str(reminder) +'" to '+ str(cnt) + ' numbers')
        return "Success"

# def getUserFromRef(refcode):
#     #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#     name = getRow(refcode);
#     #name = sheetList[row][1]
#     return name

# def getRow(uid):

#     rlen = len(sheetList)
#     clen = len(sheetList[0])
#     peeps = {}
#     cnt = 0
#     namerow = 0
#     new = True

#     for row in range(rlen):
#         if row == 0:
#             continue
#         cnt += 1
#         zerocell = sheetList[row][0]
#         #print "uid zerocell",uid,zerocell
#         if str(uid) == str(zerocell):
#             #print "uid zerocell",uid,zerocell
#             new = False
#             #print "new is ",new
#             break
        
#     if(new):
#         row = cnt+2
#         #sheet.update_cell(row, 2, "unknown user") # pos message
#         name = "Team COMM!T"
#     else:
#         row = cnt
#         name = sheetList[row][1]

#     return name

# def writeMessageToDB(message):
#     # use creds to create a client to interact with the Google Drive API

#     row = 2
#     #row = getRow(uid)

#     sheet.update_cell(row, 4, message) # pos message

#     return message

# def writeMessageToDB2(message):
#     # use creds to create a client to interact with the Google Drive API

#     row = 2
#     #row = getRow(uid)

#     sheet.update_cell(row, 5, message) # pos message

#     return message

# def writeUserToDB(message):
#     # use creds to create a client to interact with the Google Drive API
#     ### save longtoken to db along with uid and whatever else ###
#     rlen = len(sheetList)
#     clen = len(sheetList[0])
#     peeps = {}

#     for row in range(rlen):
#         if row == 0:
#             continue
#         tmp = []
#         for i in range(1,4):
#             tmp.append(sheetList[row][i])
#         peeps[sheetList[row][0]] = tmp

#     cnt = 0
#     new = True
#     for key, val in peeps.items():
#         cnt += 1
#         if key == message:
#             new = False
#             break 
#     #cnt+1 is current user, cnt+2 will write new line
#     row = 0
#     if(new):
#         row = cnt+2
#     else:
#         row = cnt+1
#     sheet.update_cell(row, 1, message) # pos message

#     return 'success'



# def writeAll(json_dict):
#     uid = json_dict['uid']
#     longToken = json_dict['longToken']
#     friends = ''
#     timeStamp = datetime.datetime.now()
#     message1 = ""
#     message2 = ""

#     row = getRow(uid)
#     sheet.update_cell(row, 2, timeStamp)
#     sheet.update_cell(row, 3, longToken)
#     sheet.update_cell(row, 8, friends)
#     sheet.update_cell(row, 4, message1)
#     sheet.update_cell(row, 5, message2)

#     return 'writeAll succeeded'


# get persistent layer as list of lists
# def pLayer():
#     # Find a workbook by name and open the first sheet
#     # Make sure you use the right name here.
#     # use creds to create a client to interact with the Google Drive API
#     scope = ['https://spreadsheets.google.com/feeds']
#     creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#     client = gspread.authorize(creds)
#     sheet = client.open("VoteBot App").sheet1
#     # Extract and print all of the values
#     #list_of_vals = sheet.get_all_values()
#     return sheet


# def people():
#     # use creds to create a client to interact with the Google Drive API
#     scope = ['https://spreadsheets.google.com/feeds']
#     creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#     client = gspread.authorize(creds)
    
#     sheet = client.open("commitDB").sheet1
#     sheetList = sheet.get_all_values()
#     rlen = len(sheetList)
#     clen = len(sheetList[0])
#     peeps = {}
#     for row in range(rlen):
#         if row == 0:
#             continue
#         tmp = []
#         for i in range(1,10):
#             tmp.append(sheetList[row][i])
#         peeps['+' + sheetList[row][0]] = tmp
#     return peeps
        
# peoples = people()
# print(peoples)
# print('Done!')



