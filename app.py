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
	print me
	return "worked"
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)