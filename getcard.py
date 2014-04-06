import json
import date
import time
import datetime
import Queue

#so basically you want to setup the priority queue, then you retrieve all the people, and insert all of them

def setup():
    flashcards = Queue.PriorityQueue()

#intervals based on 30s, 2m, 5m, 15m, 1h, 5h, 1d, 5d, 25d, 2mo.
interval={1:30,2:120,3:300,4:900,5:60*60,6:5*60*60,7:24*60*60,8:5*24*60*60,9:25*24*60*60,10:60*24*60*60}

#inserts the flashcard into the flashcard queue based on correct or incorrect response given by user
def insert(flashcard, flashcards, response=1):
    #delta_stage is the change in the memorization stage based on response & current stage
    if flashcard["stage"] < 5:
        if response == true:
            delta_stage = 1
        else:
            delta_stage =- 1
    else:
        if response == true:
            delta_stage = 2
        else:
            delta_stage =- 2
    flashcard["stage"] += delta_stage
    flashcard["time"] = time.time() + interval[flashcard["stage"]]
    flashcards.put(flashcard["time"], flashcard)

#retrieve num of flashcards
def retrieve(num):
    #paras better get this shit or i'm gonna spank his ass
    #return list of JSON

#inserts all of the retrieved JSON into queue
def insertall(retrievedlist, flashcards):
    for flashcard in retrievedlist:
        insert(flashcard, flashcards)

#some thing along the lines of this...
def run():
    currentflashcard = None
    while(1):
        currenttime = time.time()
        if currentflashcard is None:
            currentflashcard = flashcards.get()
        #just in case there are time hiccups, i'll add in a 10 second threshold...sue me
        if currentflashcard["time"] - currenttime < 10:
            #do something? like push a notification idk LOL
            currentflashcard = None

