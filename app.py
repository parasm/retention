from flask import Flask, render_template, request, redirect, session
import jinja2
import os
import facebook
from pymongo import MongoClient
import sendgrid
from twilio.rest import TwilioRestClient
import time
import requests
from bson.objectid import ObjectId

client = MongoClient("mongodb://admin:pretzelssux201@oceanic.mongohq.com:10099/retention")
db = client.get_default_database()
users = db.users
flashcards = db.flashcards

app = Flask(__name__)
app.secret_key = 'paras_is_the_slim_reaper'


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

interval={1:30,2:120,3:300,4:900,5:60*60,6:5*60*60,7:24*60*60,8:5*24*60*60,9:25*24*60*60,10:60*24*60*60}

#inserts the flashcard into the flashcard database based on correct or incorrect response given by user
def insert(flashcard, response=True):
    #delta_stage is the change in the memorization stage based on response & current stage
    if flashcard["stage"] < 5:
        if response == True:
            delta_stage = 1
        else:
            delta_stage =- 1
    else:
        if response == True:
            delta_stage = 2
        else:
            delta_stage =- 2
    flashcard["stage"] += delta_stage
    flashcard["time"] = time.time() + interval[flashcard["stage"]]
    result = flashcards.find({"id":flashcard["id"]}).limit(1)[0]
    if result == None:
        flashcards.insert(flashcard)
    else:
        flashcards.update({"_id":result["_id"]},flashcard)
def insertall(user):
    for flashcard in user["flashcards"]:
    	insert(flashcard)

@app.route('/')
def hello():
	session.pop('token',None)
	session.pop('user',None)
	return render_template("index.html", page='signup')
@app.route('/login')
def user():
	user = facebook.get_user_from_cookie(request.cookies,'1420579554861962','b1ffcae9099845e428322a88193bc072')
	try:
		token = user.get('access_token')
		session['token'] = token
	except AttributeError, e:
		return redirect('/')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	print profile
	try:
		person = users.find({"fb_id":profile.get('id')})[0]
	except IndexError, e:
		users.insert({"username":profile.get('username'),"first_name":profile.get('first_name'),"last_name":profile.get('last_name'),
		"email":profile.get('email'),"fb_id":profile.get('id'),'flashcards':[], 'extensions':[]})
		session['user'] = profile.get('id')
		return redirect('/decks')

	session['user'] = person.get('fb_id')
	print person.get('id')
	return redirect('/decks')
	# me = profile.get('first_name') +" "+ profile.get('last_name')
	# friends = graph.get_connections("me", "friends").get('data')
	# groups = graph.get_connections("me","groups").get('data')
	# all_people = []
	# gs = []
	# for g in groups:
	# 	#print graph.get_object(g.get('id'))
	# 	gs.append(g.get('id'))
	# 	all_people.append(graph.get_connections(g.get('id'),"members"))
	# return render_template('list.html',groups=gs, people=all_people,count=len(groups))
@app.route('/decks',methods=['GET','POST'])
def decks():
	user = session.get('user')
	#token = session.get('token')
	if user:
		person = users.find({"fb_id":user})[0]
		decks = person.get('flashcards')
		reminders = flashcards.find({'reminded':True,'fb_id':user})
		reminders_getted = []
		for i in reminders:
			reminders_getted.append(i)
		# if flashcards:
		return render_template('decks.html',decks=decks,reminders=reminders_getted)
		# else:
			# return redirect('/add_decks')
	else:
		return redirect('/')
@app.route('/study/<uid>')
def study(uid):
	from_db = flashcards.find({"_id":ObjectId(uid)})
	if not from_db:
		return redirect('/decks')
	return render_template('study.html',flashcards=from_db)
@app.route('/notify')
def notify():
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
			#print("sent placeholder")
			if card["reminded"] == False:
				sendgrid_notification(user, len(flashcards_due))
				twilio_notification(user, len(flashcards_due))
@app.route('/add_decks',methods=['GET','POST'])
def add_decks():
	return render_template('add_decks.html')
@app.route('/add_decks/facebook',methods=['GET','POST'])
def face():
	token = session.get('token')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	groups = graph.get_connections("me","groups").get('data')
	all_people = []
	gs = [groups]
	print gs
	group_count = []
	for g in groups:
		group_count.append(len(graph.get_connections(g.get('id'),"members").get('data')))
	return render_template('facebook.html', groups=groups,group_count=group_count)
@app.route('/add_decks/facebook/<id>')
def facebook_id(id):
	token = session.get('token')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	group =  graph.get_object(id)
	members = graph.get_connections(id,"members").get('data')
	flash = []		
	for p in members:
		image_url ='https://graph.facebook.com/'+p.get('id')+'/picture'
		flash.append({'question':{'type':'image','value':image_url},'answer':{'type':'text','value':p.get('name')},'attempts':0,'stage':0,'time':int(time.time())})
	id = flashcards.insert({'username':profile.get('username'),'cards':flash,'deck_name':group.get('name'),
		'reminded':True,'fb_id':profile.get('id')})
	person = users.find({'fb_id':profile.get('id')}).limit(1)[0]
	person['flashcards'].append({'time':time.time(),'username':profile.get('username'),'cards':flash,
		'deck_name':group.get('name'),'fb_id':profile.get('id')})
	users.update({'fb_id':profile.get('id')},person)
	return redirect('/decks')
@app.route('/add_decks/custom',methods=['GET','POST'])
def custom():
	token = session.get('token')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	user = users.find({'fb_id':profile.get('id')})[0]
	extras = user['extensions']
	return render_template('custom.html', extras=extras)
@app.route('/add_decks/plain',methods=['GET','POST'])
def plain():
	return render_template('plain.html')
@app.route('/insert',methods=['GET','POST'])
def inserty():
	if request.method == "POST":
		user = request.form.get('user')
		print user
		return redirect('/')
@app.route('/extensions', methods=['GET','POST'])
def extend():
	token = session.get('token')
	if request.method == "POST":
		code = request.form.get('code')
		name = request.form.get('name')
		graph = facebook.GraphAPI(token)
		profile = graph.get_object("me")
		user = users.find({'fb_id':profile.get('id')})[0]
		user['extensions'].append({"name":name,'code':code})
		users.update({'fb_id':profile.get('id')},user)
		return redirect('/decks')
	return render_template('extensions.html')
@app.route('/token',methods=['GET','POST'])
def get_token():
	if request.method == "POST":
		access_token = request.form.get('token')
		phone_id = request.form.get('phone_id')
		print access_token
		print phone_id
		try:
			token = access_token
			session['token'] = token
		except AttributeError, e:
			return redirect('/')
		graph = facebook.GraphAPI(token)
		profile = graph.get_object("me")
		print profile
		try:
			person = users.find({"fb_id":profile.get('id')})[0]
		except IndexError, e:
			users.insert({"username":profile.get('username'),"first_name":profile.get('first_name'),"last_name":profile.get('last_name'),
			"email":profile.get('email'),"fb_id":profile.get('id'),'flashcards':[]})
			session['user'] = profile.get('id')
			return redirect('/decks')
		return "Recieved"
	return "recieved"
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)