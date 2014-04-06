#check every minute which flashcards are "due"
from pymongo import MongoClient
import requests
import time
import sendgrid
from twilio.rest import TwilioRestClient

client = MongoClient("mongodb://admin:pretzelssux201@oceanic.mongohq.com:10099/retention")
db = client.get_default_database()
users = db.users
flashcards = db.flashcards

def sendgrid_notification(user, numcards):
	sg = sendgrid.SendGridClient('parasm','bcabooks')
	body = 'It\'s time to study. You have ' + str(numcards) + ' flashcards that you should take a look at.\n http://getretention.herokuapp.com/'
	message = sendgrid.Mail(to=user["email"], subject='GetRetention reminds you to study!', html=body, text=body, from_email='info@getretention.herokuapp.com')
	status, msg = sg.send(message)

def twilio_notification(user, numcards):
	account = "AC36ddf2336e764b488e813b2941ebfe45"
	token = "ecbf476f594fefae357cbb70839a5c37"
	client = TwilioRestClient(account,token)
	body = 'It\'s time to study. You have ' + str(numcards) + ' flashcards that you should take a look at.\n http://getretention.herokuapp.com/'
	message = client.messages.create(to="+12019626168", from_="+15704378644", body=body)

twilio_notification(None, 132)
#collects all the cards that are currently due for notification and stores them in a list
def gather():
	current_time = time.time()
	for user in users.find({}):
		print(user["username"])
		for flashcard in user["flashcards"]:
			flashcards_due = []
			for card in flashcard["cards"]:
				#print(card)
				if card["time"] <= current_time:
					flashcards_due.append(card)
					card["reminded"] = True
					flashcards.update({'fb_id':card.get('id')},card)
			#sendgrid_notification(user, len(flashcards_due))

# message = "the test message"
# tickerText = "ticker text message"
# contentTitle = "content title"
# contentText = "content body"
# registrationIdsarray = ["22854d176309401b"]
# message = {"message":"test message", "tickerText":"ticker text", "contentTitle":"content title", "contentText":"content text"}

# apikey = "AIzaSyC8nTBE2YYGl2Xm7bHg-kqqthZmi8Cja3A"
# def push_notification(apikey, registrationIdsarray, message):
# 	headers = {"Content-Type" : "application/json", "Authorization" : "key=" + apikey}
# 	data = {"data":message, "registration_ids":registrationIdsarray}

# 	r = requests.post(url="https://android.googleapis.com/gcm/send",verify=False, headers=headers,data=data)
# 	print(r)
# 	return r
#print(gather())
