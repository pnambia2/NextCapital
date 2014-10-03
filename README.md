NextCapital Todo List
=====================

This is a simple web app that allows users to create and maintain a todo list.

It takes advantage of the NextCapital API described here: http://recruiting-api.nextcapital.com


Solution 
-------------

At the moment, the web app allows users to do the following things:

* Sign up
* Log in
* See a list of their todos
* Create new todos
* Mark todos as complete
* Reorder their todos (Note: This is just a client side reordering. Upon signing out and signing back in, the ordering is not preserved.)

Technology and Tools
------------------------------

For the web app, I have used the following tools extensively:
* Flask, a Python web micro framework
* NextCapital API as required
* Python requests library to make HTTP requests (GET, PUT, POST, DELETE)
* Bootstrap to make my front end a little more presentable


Notes
---------

I understand that this web app is far from perfect. In particular, upon any kind of refresh (including hitting 'Completed'), the client side ordering is no longer preserved. If I had more time, I would change a number of things. I enjoyed working with the API, and I think that this is a neat interview problem.
