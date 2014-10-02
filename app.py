import os
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, g
import requests
import json

# These are global variables that I use to keep track of the session

api_token = ""
user_id = -1
todos = []
email = ""
todo_list = []

app = Flask(__name__)


@app.route('/')
def index():
	#The home page
	
	return render_template('index.html')

@app.route('/signup/')
def signup():
	#The sign up page
	
	return render_template('signup.html')


@app.route('/signup/submitdata/', methods = ['POST'])
def signup_submit():
	#On clicking submit, redirects to this page, does the actual API call
	
	
	email = request.form['email']
	password = request.form['password']
	
	signup_url = "http://recruiting-api.nextcapital.com/users"
	data = {"email": email, "password": password}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	r = requests.post(signup_url, data=json.dumps(data), headers=headers)	# Using the requests library to sign the user up
	
	if r.json()['email'] == [u'has already been taken']:
		return redirect('/user_taken/')								# Redirect to page that tells the user that the email is taken

	return redirect('/')

@app.route('/user_taken/')
def user_taken():
	#Page to tell the user that the email is taken
	
	return render_template('user_taken.html')

@app.route('/signin/')
def signin():
	#Page to sign in
	
	return render_template('signin.html')

@app.route('/signin/submitdata/', methods = ['POST'])
def signin_submit():
	#Does the actual API call for sign in
	
	global api_token
	global user_id
	global todos
	global email

	email = request.form['email']
	password = request.form['password']

	signin_url = "http://recruiting-api.nextcapital.com/users/sign_in"
	data = {"email": email, "password": password}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	r = requests.post(signin_url, data=json.dumps(data), headers=headers)		# Using requests lib to sign in

	
	if 'error' in r.json():
		if r.json()['error'] == "Couldn't find a user with that email.":		# Email doesnt exist
			return redirect('/user_invalid/')
	
		elif r.json()['error'] == "Password is not valid.":						# Invalid pw
			return redirect('/user_invalid/')
	
	else:
		api_token = r.json()['api_token']
		user_id = r.json()['id']
		todos = r.json()['todos']
		email = r.json()['email']					# update global variables if the sign in was successful
		
		return redirect('/todos/')

@app.route('/user_invalid/')
def user_invalid():
	#Invalid pw or the email was taken
	
	return render_template('user_invalid.html')

@app.route('/todos/', methods = ['GET'])
def todos():
	#API call to get todos for my user
	
	global todo_list
	
	url = "http://recruiting-api.nextcapital.com/users/{}/todos.json?api_token={}".format(str(user_id), str(api_token))
	

	headers = {'Content-type': 'application/json'}

	r = requests.get(url, headers = headers)

	todo_list = r.json()

	return redirect('/todos/display/')

@app.route('/todos/display/')
def display_todos():
	#Actually displays the todo list
	
	return render_template('todo_list.html', todo_list = todo_list)

@app.route('/todos/newitem/', methods = ['POST', 'GET'])
def new_item():
	#API call to add new item, redirects to the todos/display

	description = request.form['desc']
	url = "http://recruiting-api.nextcapital.com/users/{}/todos".format(str(user_id))
	
	
	data = {"api_token": api_token, "todo": {"description": description}}

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	r = requests.post(url, data=json.dumps(data), headers=headers)
		
	return redirect('/todos/')

@app.route('/todos/<int:todo_id>', methods = ['POST', 'GET'])
def mark_completed(todo_id):
	#API call to update an item's complete status to TRUE
	
	url1 = "http://recruiting-api.nextcapital.com/users/{}/todos/{}?api_token={}".format(str(user_id), str(todo_id), str(api_token))

	headers = {'Content-type': 'application/json'}

	r1 = requests.get(url1, headers = headers)

	description = r1.json()['description']

	url2 = "http://recruiting-api.nextcapital.com/users/{}/todos/{}".format(str(user_id), str(todo_id))
	
	data = {"api_token": api_token, "todo": {"description": description, "is_complete": "true"}}
	
	
	r2 = requests.put(url2, data = json.dumps(data), headers = headers)
	

	return redirect('/todos/')

@app.route('/todos/up/<int:todo_id>')
def move_up(todo_id):
	#Moves the item higher in the list
	global todo_list

	for index in range(0, len(todo_list)):
		if todo_list[index]['id'] == todo_id:
			break;
	
	if index != 0:	# dont move the first element up
		todo_list[index], todo_list[index-1] = todo_list[index-1], todo_list[index]		#swap



	return redirect('/todos/display/')

@app.route('/todos/down/<int:todo_id>')
def move_down(todo_id):
	#Moves the item lower in the list
	global todo_list
	
	for index in range(0, len(todo_list)):
		if todo_list[index]['id'] == todo_id:
			break;
	
	if index != (len(todo_list)-1):		#dont move the last element down
		todo_list[index+1], todo_list[index] = todo_list[index], todo_list[index+1]		#swap
		
	return redirect('/todos/display/')

@app.route('/signout/')
def sign_out():
	#API call to signout, redirects to homepage 
	global api_token
	global user_id
	global todos
	global email
	global todo_list
	
	url = "http://recruiting-api.nextcapital.com/users/sign_out"
	headers = {'Content-type': 'application/json'}
	data = {"api_token": api_token, "user_id": user_id}

	r = requests.delete(url, data = json.dumps(data), headers = headers)

	api_token = ""
	user_id = -1
	todos = []				#reset the value on sign out
	email = ""
	todo_list = []

	return redirect('/')





if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)			#for heroku
