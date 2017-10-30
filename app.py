from flask import Flask, request, redirect, jsonify, render_template
from flask_cors import CORS, cross_origin
# from twilio.twiml.messaging_response import MessagingResponse
from scrape import ping, people, pLayer, extendToken, writeMessageToDB, writeUserToDB, writeAll
import random
import threading
import datetime
import re
# from twilio.rest import Client
from string import punctuation
import requests
import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
	out = ''
	try:
		page_name = 'fancycommitlogin'
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
        stuff = writeAll(uid, longToken, friends, timeStamp, message1, message2)


        data = {'uid': uid, 'longToken': longToken}

        return stuff
    else:

        return "Something sent a non-post request to apiTest"

if __name__ == "__main__":
	app.run(debug=False)
