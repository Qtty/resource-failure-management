from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from utility import check_args
from database.db_api import db
from responsable import check_if_resp_decorator
from responsable import check_if_resp_of_ressource


class Resources(Resource):

    get_args = [
        '_id'
    ]

    put_args = [
        'desc',
        'loc'
    ]

    delete_args = [
        '_id'
    ]

    def get(self):
        if not check_args(dict(request.args), *self.get_args):
            return "Missing Arguments", 400

        data = dict(request.args)

        res = db.resources().get_resource(data['_id'])
        if res:
            return res, 200

        return None, 404

    @check_if_resp_decorator
    def put(self):
        if not check_args(request.get_json(), *self.put_args):
            return "Missing Arguments", 400

        data = request.get_json()

        res = db.resources().add_resource(data['desc'], data['loc'], get_jwt_identity())

        return res, 200

    @check_if_resp_decorator
    def delete(self):
        if not check_args(request.get_json(), *self.delete_args):
            return "Missing Arguments", 400

        data = request.get_json()

        if check_if_resp_of_ressource(data['_id'], get_jwt_identity()):
            db.resources().delete_resource(data['_id'])

            return '', 200

        return {'error': 'Pas Autoriser pour le resource demander'}, 401