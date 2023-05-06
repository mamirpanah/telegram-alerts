Python REST-API Development with Flask for sending Grafana Alerts to Telegram channels.
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

    $ git clone https://github.com/mamirpanah/telegram-alerts.git
    $ cd telegram-alerts
    $ python3 -m venv venv
    $ . venv/bin/activate
    (venv) pip install -r requirements.txt
    $ export TELEGRAM_TOKEN="<your_token_here>"
    $ flask run -h 0.0.0.0 -p 5000

finished


Installation with docker
------------

    $ docker build -t restapi-alerts:1 .
    $ docker run --rm -it -p 8080:5000 -e TELEGRAM_TOKEN="<your_token_here>" python_flask:1 flask run -h 0.0.0.0 -p 5000

Installation with docker-compose
------------
    $ echo 'TELEGRAM_TOKEN="<your_token_here>"' > .env
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
Creating a REST API for POST request on http://127.0.0.1:8686/api/v1/telegramalerts

All the things that you should change is in restapi/resource :
1. git clone https://github.com/mamirpanah/telegram-alerts.git
2. cd telegram-alerts/restapi/resource/apiv1
3. vim __init__.py
4. vim user.py

Step 3 in detail:

__init__.py
```
from restapi.app import apiv1 as api
from restapi.resource.apiv1.user import UserResource

api.add_resource(
	UserResource,
	"/telegramalerts",
	methods=["GET", "POST"],
	endpoint="telegramalerts"  # It will be shown in response as key name.
)
```

Everytime you want to add or change an endpoint like "/telegram-alerts" you should add_resource() by calling api object with desired arguments, for example:
* The first argument is the class that contains get, post or put methods definitions, that is present in user.py file
* The second argument is the endpoint url itself
* The 3rd argument shows the methods that api endpoint accepts for incoming requests

Step 4 in detail:

user.py
```
from flask_restful import Resource
from restapi.util import jsonify
import telebot
import os
from flask import request

bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"], parse_mode=None)

class UserResource(Resource):

	def get(self, user_id=None):
		"""
		GET /telegramalerts --> Get list of users.
		"""
		pass

	def post(self):
		"""
		POST /telegramalerts --> Send new alerts.
		"""
		data = request.get_json(force=True)
		chat_id = data.get("chatID",None)
		message = data.get("msg",None)
		bot.send_message(chat_id=chat_id, text=message)
		return jsonify({
			"quote": message
			})
		

	def patch(self, user_id):
		"""
		PATCH /telegramalerts --> Not allowed.
		"""
		pass

	def delete(self, user_id):
		"""
		DELETE /telegramalerts --> Not allowed.
		"""
		pass
```

In step 3 we called UserResource as the class for POST requests, now with modifying post definition you can call other functions to do whatever you want and finally take back a response, it means you can import other packages in user.py file and use them in "post" method definition by calling it. For example, we have imported `import telebot` and created an instance of the bot `bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"], parse_mode=None)` and for every post requests coming to our api the function `bot.send_message(chat_id=chat_id, text=message)` is called with "chat_id" that is the ID of Telegram channel that you want to send alerts, and the "message" is the body content of the alert.

Finally to test the created api:

	curl -H "Content-Type: application/json" -X POST http://127.0.0.1:8686/api/v1/telegramalerts -d "{\"msg\": \"testing the api\", \"chatID\": \"-1001636106513\"}"

{
    "quote": "testing the api",
    "message": "OK",
    "code": 100
}

How to use telegram-alerts quickly:
------------

1. Create a telegram bot with @BotFather and get the access token.
2. Replace the access token of .env file.
3. Create a Telegram channel, and add the bot you just created and make it admin of the channel.
4. find the chat ID of the channel by forwarding a message to @chatIDrobot
5. To install this api, go to your monitoring server: 1-`git clone https://github.com/mamirpanah/telegram-alerts.git`  2-`cd telegram-alerts/` 3-`echo 'TELEGRAM_TOKEN="<your_token_here>"' > .env` and finnaly 4-`docker-compose up -d --build`
6. Finnaly to send an alert as a test: `curl -H "Content-Type: application/json" -X POST http://127.0.0.1:8686/api/v1/telegramalerts -d "{\"msg\": \"testing the api\", \"chatID\": \"<your_chat_id>"}"`
