import json
import date
import time
import datetime
import Queue
#intervals based on 30s, 2m, 5m, 15m, 1h, 5h, 1d, 5d, 25d, 2mo.
interval={0:30,1:120,2:300,3:900,4:60*60,5:5*60*60,6:24*60*60,7:5*24*60*60,8:25*24*60*60,9:60*24*60*60}
#inserts the flashcard into the flashcard queue based on correct or incorrect response given by user
def insert(flashcard, flashcards, response):
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


    
