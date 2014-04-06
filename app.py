from flask import Flask, render_template, request, redirect, session
import jinja2
import os
import facebook
from pymongo import MongoClient
import sendgrid
from bson.objectid import ObjectId

client = MongoClient("mongodb://admin:pretzelssux201@oceanic.mongohq.com:10099/retention")
db = client.get_default_database()
users = db.users

app.secret_key = 'paras_is_the_slim_reaper'

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("index.html")
@app.route('/login')
def user():
	user = facebook.get_user_from_cookie(request.cookies,'1420579554861962','b1ffcae9099845e428322a88193bc072')
	try:
		token = user.get('access_token')
	except AttributeError, e:
		return redirect('/')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	print profile
	person = users.find({"fb_id":profile.get('id')})[0]
	if person == None:
		users.insert({"username":profile.get('username'),"first_name":profile.get('first_name'),"last_name":profile.get('last_name'),
		"email":profile.get('email'),"fb_id":profile.get('id'),'flashcards':[]})
		session['user'] = profile.get('id')
		return redirect('/decks')
	else:
		session['user'] = person.get('id')
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
	if user:
		return "decks"
	else:
		return redirect('/')
@app.route('/add_decks',methods=['GET','POST'])
def add_decks():
	return "paras"

@app.route('/token',methods=['GET','POST'])
def get_token():
	if request.method == "POST":
		access_token = request.form.get('token')
		print access_token
		return "Recieved"
	return "recieved"
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)