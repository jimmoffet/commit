from flask import Flask, request, redirect, jsonify, render_template
from flask_cors import CORS, cross_origin
# from twilio.twiml.messaging_response import MessagingResponse
from scrape import extendToken
from scrapeNEW import sendSMS, sendReminderSMS
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
import time



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
		return render_template('login.html', refname=name, refcode=0)
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
			msg.html = render_template('COMM!T Template.html', name=user.name, referring_user=referring_user.name, ref_link='https://www.commit.vote/r/' + str(user.id))
			mail.send(msg)

	return "Sent"

@app.route("/mail/links")
def sendlinks():

	users = User.query.filter_by(distFromPoll=None).all()
	emailed_users = set([])

	if len(users) != 0:
		with mail.connect() as conn:
			for user in users:
				if user.email not in emailed_users:
					referring_user = User.query.get(user.referringUser)
					subject = "COMM!T: Check in time"
					msg = Message(recipients=[user.email], subject=subject, sender='teamcommitapp@gmail.com')
					msg.html = render_template('COMM!T check-in.html', name=user.name, referring_user=referring_user.name, checkin_link='https://www.commit.vote/checkin/' + str(referring_user.id) + 'A' + str(user.id))

					# if user.phone != None:
					# 	try:
					# 		sendReminderSMS(user.phone,referring_user.name,str(referring_user.id),str(user.id))
					# 	except Exception as e:
					# 		print(e)

					try:
						conn.send(msg)
						emailed_users.add(user.email)
					except:
						emailed_users.add(user.email)
						print(user.email)
				#time.sleep(5) 

	return "Sent"

@app.route("/sms/links")
def sendSMSlinks():

	users = User.query.filter_by(distFromPoll=None).all()
	sent_users = set([])
	print(users)

	if len(users) != 0:
		for user in users:
			print('attempting user')
			print(user.id)
			if user.phone not in sent_users:
				try:
					referring_user = User.query.get(user.referringUser)
				except:
					referring_user = User.query.get('0')
					print('GETTING REFERRING USER FAILED')
				print('attempting a phone')
				print(user.phone)
				print(user.name)
				if user.phone != None:
					try:
						sent_users.add(user.phone)
						sendReminderSMS(user.phone,referring_user.name,str(referring_user.id),str(user.id))
					except Exception as e:
						print(e)
						sent_users.add(user.phone)
					else:
						print('call to sendReminderSMS worked')
						print(user.phone)

	return "Sent"

@app.route("/mail/debriefs")
def senddebriefs():

	users = User.query.all()
	emailed_users = set([])
	count = 0

	if len(users) != 0:
		with mail.connect() as conn:
			for user in users:
				if user.id < 12:
					print(user.name)
					#referrals = User.query.filter_by(referringUser=str(user.id)).all()
					referrals = []
					for tmpuser in users:
						if tmpuser.referringUser == str(user.id):
							referrals.append(tmpuser)

					wins = []
					fails = []
					for referral in referrals:
						if referral.distFromPoll != None:
							wins.append(referral.name + ' (distance from poll: ' + referral.distFromPoll + ' )')
						else:
							fails.append(referral.name)

					print('referrals are ')
					print(referrals)

					voted = user.distFromPoll
					if user.email not in emailed_users and len(referrals) != 0 and user.referringUser != None:
						count += 1
						print(count)
						subject = "COMM!T: Election Day Debrief"
						referring_user = User.query.get(user.referringUser)
						msg = Message(recipients=[user.email], subject=subject, sender='teamcommitapp@gmail.com')
						msg.html = render_template('COMM!T Debrief.html', voted=voted, name=user.name, wins=wins, fails=fails, referring_user=referring_user.name)

						try:
							conn.send(msg)
							print('message sent')
							emailed_users.add(user.email)
						except:
							emailed_users.add(user.email)
							print('message failed'+user.email)
					#time.sleep(5) 

	return "Sent"

@app.route("/initialize", methods=["POST", "GET"])
def initdb():
	user = User('TEAM COMM!T')
	user.email = 'jimmoffet@gmail.com'
	db.session.add(user)
	db.session.commit()
	return 'success'

@app.route("/emaillist")
def emaillist():
	users = User.query.all()
	emails = []
	for user in users:
		emails.append(user.email)

	print_to_screen = ', '.join(emails)
	return print_to_screen

@app.route("/r/<string:refcode>", methods=["POST", "GET"])
def renderLogin(refcode):

    if refcode:
        refcode = refcode
        refname = User.query.get(refcode).name
    else:
        refcode = 0

    return render_template('login.html', refcode=refcode, refname=refname)

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

@app.route("/checkin/<string:refcode>", methods=["POST", "GET"])
def renderCheckin(refcode):

	if refcode:
		data = refcode.split('A')
		refcode = data[0]
		userId = data[1]
		name = User.query.get(refcode).name
	else:
		name = "TEAM COMM!T"

	return render_template('checkin.html', referring_user=name, refcode=refcode, current_user=userId)

@app.route("/checkedin/<string:refcode>", methods=["POST", "GET"])
def renderCheckedin(refcode):

	if refcode:
		data = refcode.split('A')
		refcode = data[0]
		userId = data[1]
		dist = data[2]
		name = User.query.get(refcode).name

		currentUser = User.query.get(userId)
		print(currentUser.name)
		print(dist)

		currentUser.distFromPoll = dist

		db.session.commit()



	else:
		name = "TEAM COMM!T"

	return render_template('checkedin.html', referring_user=name, refcode=refcode, current_user=userId)

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

@app.route('/createuser', methods=["POST"])
def createUser():

	if request.method == "POST":
		json_dict = request.get_json(force=True)
		print(json_dict)

		email = json_dict['email']
		sms = json_dict['phone']
		name = json_dict['name']
		user = None
		new = False

		if email == '':
			email = '99999999999999999'
		if sms == '':
			sms = '99999999999999999'

		users = User.query.all()
		for temp_user in users:
			print('username')
			print(temp_user.name)
			print(email)
			print(sms)
			print(temp_user.email)
			print(temp_user.phone)
			if email == temp_user.email or sms == temp_user.phone:
				user = temp_user
				new = False
				print('this is an existing user')
				break
			else:
				new = True
				print('this is a new user')
		if new == True:
			user = User(name)
			db.session.add(user)
			print('add new user')


		user.name = json_dict['name']
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



		user.positiveMessage = "COMM!Tbot says, " + name + " just showed up at the polls. Score one more for democracy!"
		user.negativeMessage = "COMM!Tbot says, Oh No! " + name + " didn't show up at the polls today."

		user.date = datetime.datetime.now()
		user.triggerDate = datetime.datetime(2018, 11, 7, 7, 00)

		db.session.commit()

		#yessena 3472682813

		try:
			if json_dict['phone'] != '':
				phone = json_dict['phone']
				if phone[0] != 1:
					phone = '1'+phone
				sendSMS(phone,refname,str(user.id))
		except Exception as e:
			print("sms failed")
			print(e)

	return str(user.id)

if __name__ == "__main__":
	app.run(debug=False)
