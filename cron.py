#check every minute which flashcards are "due"
from pymongo import MongoClient
import time
client = MongoClient("mongodb://admin:pretzelssux201@oceanic.mongohq.com:10099/retention")
db = client.get_default_database()
flashcards = db.flashcards

#collects all the cards that are currently due for notification and stores them in a list
def gather():
	current_time = time.time()
	cards_due = []
	for flashcard in flashcards.find({}):
		for card in flashcard["cards"]:
			if card["time"] <= current_time and card["reminded"] == false:
				cards_due.append(card)
				card["reminded"] = true
				flashcards.update({"_id":card["_id"]},card)
	return cards_due

#reminds the user of his due flashcards
def remind(cards_due):
	#jared dont be a fuck
	return 0

message = "the test message"
tickerText = "ticker text message"
contentTitle = "content title"
contentText = "content body"
message = {"message":"test message", "tickerText":"ticker text", "contentTitle":"content title", "contentText":"content text"}

apikey = "AIzaSyC8nTBE2YYGl2Xm7bHg-kqqthZmi8Cja3A"
def push_notification(apikey, registrationIdsarray, message):
	headers = {"Content-Type" : "application/json", "Authorization" : "key=" + apikey}
	data = {"data":message, "registration_ids":registrationIdsarray}

	r = requests.post(url="https://android.googleapis.com/gcm/send",verify=False, headers=headers,data=data)
	return r

print(gather())