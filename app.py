from flask import Flask, render_template, request, redirect
import jinja2
import os
import facebook
from pymongo import MongoClient
import sendgrid
from bson.objectid import ObjectId

client = MongoClient("mongodb://admin:pretzelssux201@oceanic.mongohq.com:10099/retention")
db = client.get_default_database()
users = db.users


app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("index.html")
@app.route('/user')
def user():
	# user = facebook.get_user_from_cookie(request.cookies,'1420579554861962','b1ffcae9099845e428322a88193bc072')
	# try:
	# 	token = user.get('access_token')
	# 	print token
	# except AttributeError, e:
	# 	return redirect('/')
	token = "CAAUMAnOZBI4oBAFh6a3dZCZAh9VgremW7nTmu5Cnak4GsvmGtRuUrJhTQuqN7CY114umg2eJNMeTjHDQuTlHYPGib0piCLZCHYpd0Si1w5PCzi54ZBJjVWemExwOsD2MoRxik8YQxpqlA7VjlP0CutnfMqYKsGoB0n6y4ZCqZC9oWfzgGhgnlYZCDg2yZBSsrhnsZD"
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	me = profile.get('first_name') +" "+ profile.get('last_name')
	friends = graph.get_connections("me", "friends").get('data')
	groups = graph.get_connections("me","groups").get('data')
	for g in groups:
		#print graph.get_object(g.get('id'))
		print graph.get_connections(g.get('id'),"members")
	return "groups"
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