from datetime import datetime
import json


from flask import Response, request
from flask_restplus import Resource, abort

from services.actuation import Actuation
from api import api
from models.user import Role
from auth_utils import enable_for_roles

ns = api.namespace('actuation', description='Operations related to blog posts')

actuation_service = Actuation()


def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError('Type %s is not serializable' % type(obj))


@ns.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
class ActuationController(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad params')
    @ns.response(404, 'User not found')
    def get(self):

        client_id = 1

        try:
            actuations = actuation_service.gel_all_actuations(client_id)
            return Response(json.dumps(actuations, default=json_serial), mimetype='application/json')
        except Exception as e:
            error_msg = str(e)
            abort(400, error=error_msg)

    @ns.response(200, 'Success')
    @ns.response(400, 'Bad params')
    @ns.response(404, 'User not found')
    @enable_for_roles(request, Role.ADMIN)
    def post(self):
        args = request.json
        try:
            client_id = args['client_id']
            location_id = args['location_id']
            metering_id = args['metering_id']
            timestamp = args['timestamp']
            actuation_type_id = args['actuation_type_id']
            value = args['value']
        except KeyError:
            error_msg = "Bad request body"
            abort(400, error=error_msg)

        try:
            actuation = actuation_service.insert_new_actuation(
                client_id=client_id,
                location_id=location_id,
                metering_id=metering_id,
                actuation_type_id=actuation_type_id,
                timestamp=timestamp,
                value=value,
            )
            return Response(json.dumps(actuation, default=json_serial), mimetype="application/json")
        except Exception as e:
            error_msg = str(e)
            abort(400, error=error_msg)

    @ns.response(200, 'Success')
    @ns.response(400, 'Bad params')
    @ns.response(404, 'User not found')
    @enable_for_roles(request, Role.ADMIN)
    def put(self):
        args = request.json
        try:
            client_id = args['client_id']
            location_id = args['location_id']
            metering_id = args['metering_id']
            timestamp = args['timestamp']
            actuation_type_id = args['actuation_type_id']
            value = args['value']
        except KeyError:
            error_msg = "Bad request body"
            abort(400, error=error_msg)

        try:
            actuation = actuation_service.update_actuation(
                client_id=client_id,
                location_id=location_id,
                metering_id=metering_id,
                actuation_type_id=actuation_type_id,
                timestamp=timestamp,
                value=value,
            )
            return Response(json.dumps(actuation, default=json_serial), mimetype="application/json")
        except Exception as e:
            error_msg = str(e)
            abort(400, error=error_msg)

    @ns.response(200, 'Success')
    @ns.response(400, 'Bad params')
    @ns.response(404, 'User not found')
    @enable_for_roles(request, Role.ADMIN)
    def delete(self):
        args = request.json
        try:
            client_id = args['client_id']
            location_id = args['location_id']
            metering_id = args['metering_id']
            timestamp = args['timestamp']
            actuation_type_id = args['actuation_type_id']
        except KeyError:
            error_msg = "Bad request body"
            abort(400, error=error_msg)
        try:
            actuation_service.delete_actuation(
                client_id=client_id,
                location_id=location_id,
                metering_id=metering_id,
                actuation_type_id=actuation_type_id,
                timestamp=timestamp,
            )
            return Response(json.dumps({'message': 'OK'}, default=json_serial), mimetype="application/json")
        except Exception as e:
            error_msg = str(e)
            abort(400, error=error_msg)


@ns.route('/<actuation_type>', methods=['GET'])
class GetByActuationType(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad params')
    @ns.response(404, 'User not found')
    def get(self, actuation_type):

        try:
            actuations = actuation_service.gel_all_actuations_by_name(actuation_type)
            return Response(json.dumps(actuations, default=json_serial), mimetype='application/json')
        except Exception as e:
            error_msg = str(e)
            abort(400, error=error_msg)
