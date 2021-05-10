import json

from flask import Response, request
from flask_restplus import Resource, abort

from api import api
from services.user import UserService

ns = api.namespace('auth', description='Operations related to users')

user_service = UserService()


@ns.route('/registration', methods=['POST'])
class Registration(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad params')
    @ns.response(404, 'User not found')
    def post(self):

        args = request.json
        try:
            username = args['username']
            password = args['password']
            name = args['name']
            last_name = args['last_name']
        except KeyError:
            error_msg = "No username or password set"
            abort(400, error=error_msg)

        try:
            response = user_service.create_user(username=username, password=password, name=name, last_name=last_name)
            return Response(json.dumps(response), mimetype='application/json')
        except Exception as e:
            error_msg = str(e)
            abort(400, error=error_msg)


@ns.route('/login', methods=['POST'])
class Login(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad params')
    @ns.response(404, 'User not found')
    def post(self):

        args = request.json
        try:
            username = args['username']
            password = args['password']
        except KeyError:
            error_msg = "No username or password set"
            abort(400, error=error_msg)

        try:
            response = user_service.login(username=username, password=password)
            return Response(json.dumps(response), mimetype='application/json')
        except Exception as e:
            error_msg = str(e)
            abort(400, error=error_msg)
