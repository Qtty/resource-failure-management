from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from utility import check_args
from database.db_api import db


def check_if_admin(f):

    def wrapper(*args):
        verify_jwt_in_request()
        _id = get_jwt_identity()
        claims = get_jwt()

        res = db.users().get_user(_id=_id)
        if not claims['is_admin'] or not res['is_admin']:
            return {'auth': False}, 401

        return f(*args)

    return wrapper


class Admin(Resource):

    delete_args = [
        "_id"
    ]

    put_args = [
        "nom",
        "prenom",
        "mail",
        "password"
    ]

    @check_if_admin
    def get(self):
        return db.users().get_users(), 200

    @check_if_admin
    def put(self):
        if not check_args(request.get_json(), *self.put_args):
            return "Missing Arguments", 400

        data = request.get_json()
        
        user = {i: data[i] for i in self.put_args}
        user['is_admin'] = False
        user['is_resp'] = True
        user['nom'] = user['nom'].upper()
        user['prenom'] = user['prenom'].capitalize()

        # Check if user exists

        res = db.users().insert_user(user)

        return {'_id': res.inserted_id.binary.hex()}, 200

    @check_if_admin
    def delete(self):
        if not check_args(request.get_json(), *self.delete_args):
            return "Missing Arguments", 400

        data = request.get_json()
        db.users().delete_user(data['_id'])

        return '', 200