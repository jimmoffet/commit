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

currentUser = 0
# user = User('jared', datetime.datetime.now(), 'jrjohns@mit.edu', '3280803892', '508508393', '83082982983', '930290903', '3989809808', 'hi', 'oh no', datetime.datetime.now(), '5000')



@app.route("/")
def hello():
	out = ''
	try:
		name = 'TEAM COMM!T'
		return render_template('login.html', referring_user=name, refcode=0)
	except:
		out = ' FIX MEEEEEEEEEEEEEEEEEEEEEE!!!!.'
		return out

@app.route("/initialize", methods=["POST", "GET"])
def initdb():
	user = User('TEAM COMM!T')
	user.email = 'jimmoffet@gmail.com'
	db.session.add(user)
	db.session.commit()
	return 'success'

@app.route("/r/<string:refcode>", methods=["POST", "GET"])
def renderLogin(refcode):

    if refcode:
        refcode = refcode
    else:
        refcode = 0

    return render_template('login.html', refcode=refcode)

@app.route("/commit/<string:refcode>", methods=["POST", "GET"])
def renderCommit(refcode):

	if refcode:
		print(refcode)
		data = refcode.split('A')
		print(data)
		# refcode = data[0]
		# userId = data[1]
		name = User.query.get(refcode).name
	else:
		name = "TEAM COMM!T"
		refcode = 0
		userId = 0

	return render_template('commit.html', referring_user=name, refcode=refcode, current_user=userId)

@app.route("/share/<string:refcode>", methods=["POST", "GET"])
def renderShare(refcode):

    if refcode:
        name = User.query.get(refcode).name
    else:
        name = "TEAM COMM!T"

    return render_template('share.html', referring_user=name, refcode=refcode)

@app.route("/privacy", methods=["POST", "GET"])
def renderPrivacy(refcode):


    return render_template('privacy.html')
# @app.route('/<string:page_name>/')
# def render_static(page_name):
#     return render_template('%s.html' % page_name)

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

# @app.route("/pm", methods=["POST"])
# def pm(message):
#
# 	if request.method == "POST":
#     	json_dict = request.get_json()
#
#     return 'Success!'

# @app.route('/api', methods=["POST"])
# def apiTest():

#     if request.method == "POST":
#         json_dict = request.get_json(force=True)

#         uid = json_dict['uid']
#         longToken = json_dict['longToken']
#         friends = ''
#         timeStamp = datetime.datetime.now()
#         message1 = ""
#         message2 = ""
#         #stuff = writeAll(uid, longToken, friends, timeStamp, message1, message2)
#         success = writeAll(json_dict)

#         data = {'uid': uid, 'longToken': longToken}

#         return success

#     else:

#         return "Something sent a non-post request to apiTest"

@app.route('/createuser', methods=["POST"])
def createUser():

	if request.method == "POST":
		json_dict = request.get_json(force=True)
		print(json_dict)
		#{'name': 'James David Moffet III', 'email': 'jimmoffet@gmail.com', 'phone': '', 'fbId': '1438364989611664', 'twId': '', 'fbToken': 'EAACyc2hNZCsABAEEzv25ZBhRD6ABS45yCVyfoJZB6MXQfrkr7TX3DXknYpldZAZC3iOaYYWdOZC9ZCUsC4DJpXsZChtyvv2MOLX1baIA4mKpXYprmzcht1bte8YdE5sqww6VPpyuS5ZBDHsiHX2dmyFuy3Da81m22MHaFJOtcXzDPBV8FVwViAOkwlZAuoKw9R6xYuvmjrHOfgUgZDZD', 'twToken': '', 'referringUser': 0}

		name = json_dict['name']
		user = User(name)
		user.email = json_dict['email']
		user.phone = json_dict['phone']
		user.fbId = json_dict['fbId']
		user.twId = json_dict['twId']
		user.twToken = json_dict['twToken']
		user.referringUser = json_dict['referringUser']
		user.fbToken = ''

		if json_dict['fbToken'] != '':
			user.fbToken = extendToken(json_dict['fbToken'])

			# ref_name = User.query.get(ref_user)

		user.positiveMessage = "COMM!Tbot says, " + name + " just showed up at the polls. Score one more for democracy!"
		user.negativeMessage = "COMM!Tbot says, Oh No!" + name + " didn't show up at the polls today."

		user.date = datetime.datetime.now()
		user.triggerDate = datetime.datetime(2018, 11, 7, 7, 00)
		db.session.add(user)
		db.session.commit()

	return str(user.id)

if __name__ == "__main__":
	app.run(debug=False)
