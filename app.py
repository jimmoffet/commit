from flask import Flask, request, redirect, jsonify, render_template
from flask_cors import CORS, cross_origin
# from twilio.twiml.messaging_response import MessagingResponse
from scrape import extendToken
from scrapeNEW import sendSMS
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
from flask import Flask
from flask_mail import Mail, Message
from mailcreds import mailpassword



app = Flask(__name__)
mail = Mail(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# database config
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# mail config
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'teamcommitapp@gmail.com'
app.config['MAIL_PASSWORD'] = mailpassword
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from models import User

currentUser = 0

@app.route("/")
def hello():
	out = ''
	try:
		name = 'TEAM COMM!T'
		return render_template('login.html', referring_user=name, refcode=0)
	except:
		out = ' FIX MEEEEEEEEEEEEEEEEEEEEEE!!!!.'
		return out

@app.route("/mail", methods=["POST"])
def sendit():

	if request.method == 'POST':
		mail_params = request.get_json()
		userId = mail_params['user']
		user = User.query.get(userId)
		referring_user = User.query.get(user.referringUser)

		if user.email != '':
			msg = Message('Hello from TEAM COMM!T', sender = 'teamcommitapp@gmail.com', recipients = [user.email])
			msg.html = render_template('COMM!T Template.html', name=user.name, referring_user=referring_user.name, ref_link='https://commit.vote/r/' + str(user.id))
			mail.send(msg)

	return "Sent"

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
		data = refcode.split('A')
		refcode = data[0]
		userId = data[1]
		name = User.query.get(refcode).name
	else:
		name = "TEAM COMM!T"
		refcode = 0
		userId = 0

	return render_template('commit.html', referring_user=name, refcode=refcode, current_user=userId)

@app.route("/share/<string:refcode>", methods=["POST", "GET"])
def renderShare(refcode):

	if refcode:
		data = refcode.split('A')
		refcode = data[0]
		userId = data[1]
		name = User.query.get(refcode).name
	else:
		name = "TEAM COMM!T"

	return render_template('share.html', referring_user=name, refcode=refcode, current_user=userId)

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

@app.route("/pm", methods=["POST"])
def pm():

	if request.method == "POST":
		update_dict = request.get_json()
		userId = update_dict['user']
		positiveMessage = update_dict['positiveMessage']
		user = User.query.get(userId)
		user.positiveMessage = positiveMessage
		db.session.commit()

	return 'Success!'

@app.route("/nm", methods=["POST"])
def nm():

	if request.method == "POST":
		update_dict = request.get_json()
		userId = update_dict['user']
		negativeMessage = update_dict['negativeMessage']
		user = User.query.get(userId)
		user.negativeMessage = negativeMessage
		db.session.commit()

	return 'Success!'

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

		if json_dict['referringUser'] != '':
			refname = User.query.get(json_dict['referringUser']).name

		if json_dict['fbToken'] != '':
			user.fbToken = extendToken(json_dict['fbToken'])

		if json_dict['phone'] != '':
			phone = json_dict['phone']
			if phone[0] != 1:
				phone = '1'+phone
			sendSMS(phone,refname)

		user.positiveMessage = "COMM!Tbot says, " + name + " just showed up at the polls. Score one more for democracy!"
		user.negativeMessage = "COMM!Tbot says, Oh No!" + name + " didn't show up at the polls today."

		user.date = datetime.datetime.now()
		user.triggerDate = datetime.datetime(2018, 11, 7, 7, 00)
		db.session.add(user)
		db.session.commit()

	return str(user.id)

if __name__ == "__main__":
	app.run(debug=False)
