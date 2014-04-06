#check every minute which flashcards are "due"
import from pymongo import MongoClient
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
				flashcards.update("_id":card["_id"],card)
	return cards_due

#reminds the user of his due flashcards
def remind(cards_due):
	#jared dont be a fuck
	return 0