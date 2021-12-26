from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from utility import check_args
from database.db_api import db


def check_if_resp() -> str:
    verify_jwt_in_request()
    _id = get_jwt_identity()
    claims = get_jwt()

    res = db.users().get_user(_id=_id)
    if not claims['is_resp'] or not res['is_resp']:
        return None

    return _id


def check_if_resp_of_ressource(res_id: str, resp_id: str) -> bool:
    res = db.resources().get_resource(res_id, resp_id=resp_id)

    if res:
        return True

    return False


def check_if_resp_decorator(f):

    def wrapper(*args):
        _id = check_if_resp()
        if not _id:
            return {'auth': False}, 401

        return f(*args)

    return wrapper


class Responsable(Resource):

    get_args = [
        'type'
    ]

    post_args = [
        '_id'
    ]

    @check_if_resp_decorator
    def get(self):
        if not check_args(dict(request.args), *self.get_args):
            return "Missing Arguments", 400

        data = dict(request.args)

        if data['type'] == 'resource':
            return db.resources().get_resources(get_jwt_identity()), 200

        elif data['type'] == 'ticket':
            return db.tickets().get_tickets(get_jwt_identity()), 200

        else:
            return {'error': 'Type non reconnu'}, 400

    @check_if_resp_decorator
    def post(self):
        if not check_args(request.get_json(), *self.post_args):
            return "Missing Arguments", 400

        data = request.get_json()

        # visualise

        return '', 200