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