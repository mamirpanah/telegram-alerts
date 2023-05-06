Python REST-API Development with Flask
=================================

Requirements
------------

To install and run these examples you need:

- Python 3.3+
- python3-venv or python3-virtualenv
- git (only to clone this repository)
- docker and docker-compose ( if needed a dockerized flask app )

Installation
------------

The commands below set everything up to run the examples:

    $ git clone https://github.com/mamirpanah/flask-restapi.git
    $ cd flask-restapi
    $ python3 -m venv venv
    $ . venv/bin/activate
    (venv) pip install -r requirements.txt
    $ flask run -h 0.0.0.0 -p 5000

finished


Installation with docker
------------

    $ docker build -t python_flask:1 .
    $ docker run --rm -it -p 8080:5000 python_flask:1 flask run -h 0.0.0.0 -p 5000

Installation with docker-compose
------------

    $ docker-compose up -d --build

note: You can replace "command" of docker-compose.yml with following commands to run flask web server:
* flask run -h 0.0.0.0 -p 5000
* gunicorn -w 2 -b 0.0.0.0:5000 restapi.app:create_app
* python3 -m flask run -h 0.0.0.0 -p 5000

For production use:
------------

note: Never expose the dev server to the outside (such as binding to 0.0.0.0). Use a production WSGI server such as uWSGI or Gunicorn.

    $ gunicorn -w 2 -b 0.0.0.0:5005 restapi.app:create_app
    
    


Using factory method to import flask web server as an object into another python project:
------------


    $ import restapi
    $ app_object = restapi.create_app()
    $ app_object.run(host="0.0.0.0", port=5005)




How to customize python flask web server as a restful-api:
------------
Creating a REST API for GET request on http://localhost:5000/users

All the things that you should change is in restapi/resource :
1. git clone https://github.com/mamirpanah/flask-restapi.git
2. cd flask-restapi/restapi/resource/apiv1
3. vim __init__.py
4. vim user.py

Step 3 in detail:

__init__.py
```
from restapi.app import apiv1 as api
from restapi.resource.apiv1.user import UserResource

api.add_resource(
	UserResource,
	"/users",
	methods=["GET", "POST"],
	endpoint="users"  # It will be shown in response as key name.
)
```

Everytime you want to add or change an endpoint like "/users" you should add_resource() by calling api object with desired arguments, for example:
* The first argument is the class that contains get, post or put methods definitions, that is present in user.py file
* The second argument is the endpoint url itself
* The 3rd argument shows the methods that api endpoint accepts for incoming requests

Step 4 in detail:

user.py
```
from flask_restful import Resource
from restapi.util import jsonify

class UserResource(Resource):

	def get(self, user_id=None):
		"""
		GET /users --> Get list of users.
		GET /users/<user_id> --> Get the user.
		"""
		if user_id is None:
			return jsonify({
			"users": "test without user_id"
			})
		else:
			return jsonify({
			"users": "test with user_id"
			})

	def post(self):
		"""
		POST /users --> Create new user.
		POST /users/<user_id> --> Not allowed.
		"""
		pass

	def patch(self, user_id):
		"""
		PATCH /users --> Not allowed.
		PATCH /users/<user_id> --> Update the user.
		"""
		pass

	def delete(self, user_id):
		"""
		DELETE /users --> Not allowed.
		DELETE /users/<user_id> --> Delete the user.
		"""
		pass
```

In step 3 we called UserResource as the class for GET requests, now with modifying get definition you can call other functions to do whatever you want and finally take back a response, it means you can import other packages in user.py file and use them in "get" method definition by calling

Finally to test the created api:

	curl -H "Content-Type: application/json" -X POST http://127.0.0.1:8686/api/v1/telegramalerts -d "{\"msg\": \"testing the api\", \"chatID\": \"-1001636106513\"}"

{
    "quote": "testing the api",
    "message": "OK",
    "code": 100
}