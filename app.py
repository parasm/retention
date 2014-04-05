from flask import Flask, render_template, request, redirect
import jinja2
import os
import facebook
import pymongo
import sendgrid
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("index.html")
@app.route('/user')
def user():
	user = facebook.get_user_from_cookie(request.cookies,'1420579554861962','b1ffcae9099845e428322a88193bc072')
	print user
	try:
		token = user.get('access_token')
	except AttributeError, e:
		return redirect('/')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	me = profile.get('first_name') +" "+ profile.get('last_name')
	print dir(graph)
	friends = graph.get_connections("me", "friends").get('data')
	groups = graph.get_connections("me","groups").get('data')
	print groups
	return "friends"
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