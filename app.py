from flask import Flask, request, redirect, jsonify, render_template
from flask_cors import CORS, cross_origin
# from twilio.twiml.messaging_response import MessagingResponse
from scrape import ping, people, pLayer, extendToken, writeMessageToDB, writeUserToDB, writeAll, getUserFromRef
import random
import threading
import datetime
import re
# from twilio.rest import Client
from string import punctuation
import requests
import datetime
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# database config
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User

user = User('jared', datetime.datetime.now(), 'jrjohns@mit.edu', '3280803892', '508508393', '83082982983', '930290903', '3989809808', 'hi', 'oh no', datetime.datetime.now(), '5000')
db.session.add(user)
db.session.commit()

@app.route("/")
def hello():
	out = ''
	try:
		page_name = 'login'
		return render_template('%s.html' % page_name)
	except:
		out = ' FIX MEEEEEEEEEEEEEEEEEEEEEE!!!!.'
		return out

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

@app.route("/commit/<string:shorttoken>", methods=["POST", "GET"])
def getLongToken(shorttoken):

    resp = extendToken(shorttoken)
    #longtoken = resp['access_token']
    #print(longtoken)

    return jsonify(resp)

@app.route("/r/<string:refcode>", methods=["POST", "GET"])
def getUserFromRefcode(refcode):

    if refcode:
        name = getUserFromRef(refcode)
    else:
        name = "Team COMM!T"
    
    return render_template('commit.html', referring_user=name, my_list=[0,1,2,3,4,5])

@app.route("/positive/<string:message>", methods=["POST", "GET"])
def writePosMessage(message):

    resp = writeMessageToDB(message)

    return 'Success!'

@app.route("/negative/<string:message>", methods=["POST", "GET"])
def writeNegMessage(message):

    resp = writeMessageToDB2(message)

    return 'Success!'

@app.route("/writeuser/<string:message>", methods=["POST", "GET"])
def writeUser(message):

    resp = writeUserToDB(message)

    return 'Success!'

@app.route('/api', methods=["POST"])
def apiTest():

    if request.method == "POST":
        json_dict = request.get_json(force=True)

        uid = json_dict['uid']
        longToken = json_dict['longToken']
        friends = ''
        timeStamp = datetime.datetime.now()
        message1 = ""
        message2 = ""
        #stuff = writeAll(uid, longToken, friends, timeStamp, message1, message2)
        success = writeAll(json_dict)

        data = {'uid': uid, 'longToken': longToken}
        
        return success

    else:

        return "Something sent a non-post request to apiTest"

if __name__ == "__main__":
	app.run(debug=False)
