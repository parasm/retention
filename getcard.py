import json
import date
import time
import datetime
#intervals based on 30s, 2m, 5m, 15m, 1h, 5h, 1d, 5d, 25d, 2mo.

#inserts the flashcard into the flashcard queue based on correct or incorrect response given by user
def insert(flashcard, flashcards, response):
    #delta_stage is the change in the memorization stage based on response & current stage
    if flashcard["stage"] < 5:
        if response==true:
            delta_stage=1
        else:
            delta_stage=-1
    else:
        if response == true:
            delta_stage=2
        else:
            delta_stage=-2
    flashcard["stage"] += delta_stage

    
