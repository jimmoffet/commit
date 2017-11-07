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
import sys

# Find these values at https://twilio.com/user/account
account_sid = "AC3e1252b3f55741e9dfeb3fb4ef66d88e"
auth_token = "2e89e4f761bee93067348899cc5e6493"
client = Client(account_sid, auth_token)


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

    reminder = "COMM!Tbot says, You're committed! We'll let "+refname+" know when you check in at the polls tomorrow (or if you don't). We'll send you a few location-aware check-in reminders until you check in. Do for others what "+refname+" is doing for you with your COMM!T link: "+"http://www.commit.vote/r/"+uid

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

def sendReminderSMS(from_num,refname,uid):
    ### get phone number

    cnt=1

    reminder = "COMM!Tbot says, You're committed! We'll let "+refname+" know when you check in at the polls tomorrow (or if you don't). We'll send you a few location-aware check-in reminders until you check in. Do for others what "+refname+" is doing for you with your COMM!T link: "+"http://www.commit.vote/r/"+uid

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

def sendDebriefSMS(from_num,refname,uid,wins,fails):
    ### get phone number

    cnt=1

    reminder = "COMM!Tbot says, You're committed! We'll let "+refname+" know when you check in at the polls tomorrow (or if you don't). We'll send you a few location-aware check-in reminders until you check in. Do for others what "+refname+" is doing for you with your COMM!T link: "+"http://www.commit.vote/r/"+uid

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

wins = ['Alice','Bob','Carl']
toprint = ', '.join(wins[:-1])
print(toprint)


