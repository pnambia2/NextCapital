import os
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, g
import requests
import json

api_token = ""
user_id = -1
todos = []
email = ""
todo_list = []

app = Flask(__name__)


@app.route('/')
def index():
	
	return render_template('index.html')

@app.route('/signup/')
def signup():
	
	return render_template('signup.html')


@app.route('/signup/submitdata/', methods = ['POST'])
def signup_submit():
	print "TEST"
	email = request.form['email']
	password = request.form['password']
	
	signup_url = "http://recruiting-api.nextcapital.com/users"
	data = {"email": email, "password": password}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	r = requests.post(signup_url, data=json.dumps(data), headers=headers)
	print r.json()
	print email, password

	return redirect('/')


@app.route('/signin/')
def signin():
	
	return render_template('signin.html')

@app.route('/signin/submitdata/', methods = ['POST'])
def signin_submit():
	global api_token
	global user_id
	global todos
	global email

	email = request.form['email']
	password = request.form['password']

	signin_url = "http://recruiting-api.nextcapital.com/users/sign_in"
	data = {"email": email, "password": password}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	r = requests.post(signin_url, data=json.dumps(data), headers=headers)

	print r.json()
	
	if 'error' in r.json():
		if r.json()['error'] == "Couldn't find a user with that email.":
			return redirect('/user_noexist/')
	
		elif r.json()['error'] == "Password is not valid.":
			return redirect('/user_invalidpw/')
	
	else:
		api_token = r.json()['api_token']
		user_id = r.json()['id']
		todos = r.json()['todos']
		email = r.json()['email']
		
		return redirect('/todos/')

@app.route('/todos/', methods = ['GET'])
def todos():
	global todo_list
	print "HERE"
	print api_token
	print user_id
	
	url = "http://recruiting-api.nextcapital.com/users/{}/todos.json?api_token={}".format(str(user_id), str(api_token))
	
	print url

	headers = {'Content-type': 'application/json'}

	r = requests.get(url, headers = headers)

	todo_list = r.json()
	
	print r.text
	
	print todo_list

	return redirect('/todos/display/')

@app.route('/todos/display/')
def display_todos():
	return render_template('todo_list.html', todo_list = todo_list)

@app.route('/todos/newitem/', methods = ['POST', 'GET'])
def new_item():
	print "now here"
	print user_id

	description = request.form['desc']
	url = "http://recruiting-api.nextcapital.com/users/{}/todos".format(str(user_id))
	
	
	data = {"api_token": api_token, "todo": {"description": description}}

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	r = requests.post(url, data=json.dumps(data), headers=headers)
	print r.json()
	
	return redirect('/todos/')

@app.route('/todos/<int:todo_id>', methods = ['POST', 'GET'])
def mark_completed(todo_id):
	
	url1 = "http://recruiting-api.nextcapital.com/users/{}/todos/{}?api_token={}".format(str(user_id), str(todo_id), str(api_token))

	headers = {'Content-type': 'application/json'}

	r1 = requests.get(url1, headers = headers)

	description = r1.json()['description']

	url2 = "http://recruiting-api.nextcapital.com/users/{}/todos/{}".format(str(user_id), str(todo_id))
	
	data = {"api_token": api_token, "todo": {"description": description, "is_complete": "true"}}
	
	
	r2 = requests.put(url2, data = json.dumps(data), headers = headers)
	
	print "PRINTING TODO LIST"
	print todo_list

	return redirect('/todos/')

@app.route('/todos/up/<int:todo_id>')
def move_up(todo_id):
	global todo_list

	for index in range(0, len(todo_list)):
		if todo_list[index]['id'] == todo_id:
			break;
	
	if index != 0:
		todo_list[index], todo_list[index-1] = todo_list[index-1], todo_list[index]

	print "AFTER REORDER"
	print todo_list

	return redirect('/todos/display/')

@app.route('/todos/down/<int:todo_id>')
def move_down(todo_id):
	global todo_list
	
	for index in range(0, len(todo_list)):
		if todo_list[index]['id'] == todo_id:
			break;
	
	if index != (len(todo_list)-1):
		todo_list[index+1], todo_list[index] = todo_list[index], todo_list[index+1]
	
	print "AFTER REORDER"
	print todo_list
	
	return redirect('/todos/display/')





if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
