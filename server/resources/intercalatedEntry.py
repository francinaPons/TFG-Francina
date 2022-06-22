from flask import make_response

from server.checktype import checkType
from server.models.accounts import auth
from server.resources.nextByMode import *

from server.variable_store import *


class IntercalatedEntry(Resource):

    def get(self):
        intercalated_metadata = getVarFromFile('intercalated_metadata')
        next = json.loads(json.dumps(intercalated_metadata))
        return {'metadata': next}, 200

    @auth.login_required()
    def post(self):
        parser = reqparse.RequestParser()
        # define al input parameters need and its type
        parser.add_argument('name', type=str, required=True, help="Path  not valid: 'path' not provided")
        parser.add_argument('duration', nullable=True, help="duration  not valid: 'duration' not provided")
        parser.add_argument('type', nullable=False, help="duration  not valid: 'duration' not provided")
        dades = parser.parse_args()
        duration = None
        if checkType(dades['name']) == 'notAcceptedType':
            return make_response(("El fitxer no es multimedia", 400))
        if dades['type'] == 'Image':
            if dades['duration'] and int(dades['duration']) > 0:
                duration = int(dades['duration'])
            else:
                duration = 6000
        setVarFromFile('intercalated_metadata', {'path': "./static/" + dades['name'], 'duration': duration, 'type': dades['type']})
        return {'message': "Petició processada correctament"}, 200


    @auth.login_required()
    def delete(self):
        setVarFromFile('intercalated_metadata', {'path': "./static/default.mp4", 'duration': 0, 'type': 'video'})
        return {'message': "Petició processada correctament"}, 200


