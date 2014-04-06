#check every minute which flashcards are "due"
import from pymongo import MongoClient
import time
client = MongoClient("mongodb://admin:pretzelssux201@oceanic.mongohq.com:10099/retention")
db = client.get_default_database()
users = db.users

#collects all the cards that are currently due for notification and stores them in a list
def gather():
	current_time = time.time()
	cards_due = []
	for user in users.find({}):
		for card in user["cards"]:
			if card["time"] <= current_time and card["reminded"] == false:
				cards_due.append(card)
				card["reminded"] = true
				users.update("_id":card["_id"],card)
	return cards_due
