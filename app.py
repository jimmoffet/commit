from flask import Flask, request, redirect, jsonify, render_template
from flask_cors import CORS, cross_origin
# from twilio.twiml.messaging_response import MessagingResponse
from scrape import scrape, ping, people, pLayer, extendToken, writeToDB
import random
import threading
import datetime
import re
# from twilio.rest import Client
from string import punctuation

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
    longtoken = resp['access_token']
    print(longtoken)

    ### save longtoken to db along with uid and whatever else ###
    peoples = people()
    cnt = 0
	for key, val in peoples.items():
		cnt += 1
		if key == longtoken:
			break
   	
	#cnt+1 is 

    return jsonify(resp)

@app.route("/positive/<string:message>", methods=["POST", "GET"])
def write(message):

    resp = writeToDB(message)

    return 'Success!'

@app.route("/api")
def serve_schedule():
	schedule = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
	return jsonify(schedule)

if __name__ == "__main__":
	app.run(debug=False)
