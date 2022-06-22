from flask_restful import Resource
from flask_restful import reqparse

from server.models.accounts import auth
from server.variable_store import *


class Mode(Resource):

	def get(self):
		return {'message': getVarFromFile('mode')}, 200

	@auth.login_required()
	def put(self):
		parser = reqparse.RequestParser()  # create parameters parser from request
		parser.add_argument('mode', type=str, required=True, help="This field cannot be left blanck")
		dades = parser.parse_args()
		setVarFromFile('first', True)
		setVarFromFile('mode', dades['mode'])
		return {'message': "correct"}, 200

