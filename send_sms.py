# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import Client
from scrape import scrape, ping, people, pLayer
import sys
import datetime

# Find these values at https://twilio.com/user/account
account_sid = "AC3e1252b3f55741e9dfeb3fb4ef66d88e"
auth_token = "2e89e4f761bee93067348899cc5e6493"
client = Client(account_sid, auth_token)

### google drive api freaked out trying to read back microseconds from the sheet ###
now = datetime.datetime.now()
now = now.replace(second=0, microsecond=0)
lastsent = now - datetime.timedelta(days=7)
lastsent = lastsent.replace(second=0, microsecond=0)

go = True
row = 1
sheet = pLayer()
subscriber_list = []

while go:
	# subscriber = []
	# num = sheet.cell(row, 1).value
	# remindersent = sheet.cell(row, 15).value 
	# friendcommit = sheet.cell(row, 3).value
	# isfriend = sheet.cell(row, 7).value
	# votebotcommit = sheet.cell(row, 6).value
	# 7days = sheet.cell(row, 8).value 
	# 3days = sheet.cell(row, 9).value 
	# daybefore = sheet.cell(row, 10).value 
	

	if len(num) < 2:
		break
	else:
		if friendcommit == 'yes':
			message = "Don't forget to text your friend from the polls on November 7th!"
			subscriber = [num,remindersent,message,row]
			subscriber_list.append(subscriber)
			# sheet.update_cell(row, 12, lastsent)
			# sheet.update_cell(row, 13, lastsent)
		elif votebotcommit == 'yes':
			message = "Don't forget to vote on November 7th!"
			subscriber = [num,remindersent,message,row]
			subscriber_list.append(subscriber)
			# sheet.update_cell(row, 12, lastsent)
			# sheet.update_cell(row, 13, lastsent)
		if isfriend == 'yes':
			message = "Don't forget to make sure your friend texts you from their polling place on November 7th!"
			subscriber = [num,remindersent,message,row]
			subscriber_list.append(subscriber)
			# sheet.update_cell(row, 12, lastsent)
			# sheet.update_cell(row, 13, lastsent)
		row += 1

### check persistent layer for last sent date, if more than 7 days, send and update last sent date ###

### Currently the send time/day is set when you subscribe and will send every 7 days after that ###

#print('send_sms ran without sending')
### Iterate through subscribers ###

cnt = 0
for subscriber in subscriber_list:
	from_num = '+'+subscriber[0]
	now = datetime.datetime.now()
	now = now.replace(second=0, microsecond=0)
	if len(subscriber[1]) < 2:
		lastsent = now - datetime.timedelta(days=7)
		lastsent = lastsent.replace(second=0, microsecond=0)

	test = datetime.datetime.strptime(subscriber[1],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=7)
	# print('Found +17733541500')
	# print(from_num)
	if test < now:
		message = client.api.account.messages.create(to=from_num, from_="+16172497881", body=reminder)

		### need to add row to subscriber list so we can update the correct row

		sheet.update_cell(subscriber[5], 12, now)
		sheet.update_cell(subscriber[5], 13, now)
		cnt += 1

print('send_sms sent "'+ str(reminder) +'" to '+ str(cnt) + ' numbers')

# check for next date to send, if today send, then change date to send 
# Loop through numbers that need to recieve the message