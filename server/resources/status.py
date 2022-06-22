from flask_restful import Resource

from server.models.accounts import auth
from server.variable_store import *


class Status(Resource):
    def get(self):
        getVarFromFile('status')
        if getVarFromFile('status'):
            return {'message': "online"}, 200
        else:
            return {'message': "stop"}, 200

    @auth.login_required()
    def post(self):
        setVarFromFile('status', not getVarFromFile('status'))
        return {'message': "correct"}, 200
