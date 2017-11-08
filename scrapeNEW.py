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

def sendReminderSMS(from_num,refname,refid,uid):
    ### get phone number

    cnt=1

    if from_num != "" and from_num != None:
        if from_num[0] !=1:
            from_num = '1'+from_num

    from_num = '+'+from_num

    link = 'https://www.commit.vote/checkin/' + str(refid) + 'A' + str(uid)

    reminder = "COMM!Tbot says:\n\nThe polls are open, here's your check in link! (requires allowing location, obvs)\n\n"+link+"\n\nWe'll let "+refname+" know when you check in (or don't), so no flaking!"
    
    try:
        message = client.api.account.messages.create(to=from_num, from_="+16172497881", body=reminder)
    except Exception as e:
        #print(e)
        return e
    else:
        #print('send_sms sent "'+ str(reminder) +'" to '+ str(cnt) + ' numbers')
        return "Success"


def sendDebriefSMS(from_num,refname,uid,wins,fails,voted):
    ### get phone number
    # print(from_num,refname,uid,wins,fails,voted)
    # print(len(wins))
    # print(wins[0])

    if from_num != "" and from_num != None:
        if from_num[0] !=1:
            from_num = '1'+from_num

    cnt=1

    pwins = ''
    pfails = ''

    if len(wins) == 1:
        pwins = wins[0]+'.'
        pwins = "Friends who checked in:\n"+pwins
        print('1 triggered')

    if len(fails) == 1:
        pfails = "Friends who didn't check in:\n"+fails[0]+'.'

    if len(wins) == 2:
        tmpwins = wins[0]+' and '+wins[1]+'.'
        pwins = tmpwins
        pwins = "Friends who checked in:\n"+pwins
        print('2 triggered')

    if len(fails) == 2:
        pfails = fails[0]+' and '+fails[1]+'.'
        pfails = "Friends who didn't check in:\n"+pfails

    
    if len(wins) > 2:
        pwins = ''
        for win in wins:
            pwins = pwins+', '+win
        pwins = pwins[2:]
        pwins = "Friends who checked in:\n"+pwins+'.'
        print('3 triggered')

    
    if len(fails) > 2:
        pfails = ''
        for fail in fails:
            pfails = pfails+', '+fail
        pfails = pfails[2:]
        pfails = "Friends who didn't check in:\n"+pfails+'.'
        print('3 triggered')
        

    if voted == 'didnt':
        c = "You didn't check in and "+str(refname)+" was notified."
    else:
        c = "Nice follow through, score another one for democracy!"

    reminder = "COMM!T Election Day Debrief:\nHere's your summary. " + c + "\n\n" + pwins + "\n\n" +  pfails

    from_num = '+'+from_num

    print(from_num)
    #print(reminder)
    
    try:
        foo = 'foo'
        message = client.api.account.messages.create(to=from_num, from_="+16172497881", body=reminder)
    except Exception as e:
        print(e)
        return e
    else:
        print('send_sms sent "'+ str(reminder) +'" to '+ str(cnt) + ' numbers')
        return "Success"

# sendDebriefSMS(u'7733541500', u'TEAM COMM!T', '9', [u'James David Moffet III (distance from poll: honor-system )'], [], '30m')


