from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from utility import check_args
from database.db_api import db


class Login(Resource):

    args = [
        "mail",
        "password"
    ]

    def post(self):
        if not check_args(request.get_json(), *self.args):
            return "Missing Arguments", 400

        data = request.get_json()
        result = db.users().get_user(data["mail"], data["password"])

        if result:
            misc = {"is_admin": result['is_admin'], "is_resp": result['is_resp']}
            result = {
                "auth": True,
                "session": create_access_token(identity=result['_id'].binary.hex(), additional_claims=misc),
                "is_admin": result['is_admin'],
                "is_resp": result['is_resp']
            }
            return result, 200

        return "email ou mot de passe invalide", 403

    @jwt_required()
    def get(self):
        data = get_jwt_identity()
        claims = get_jwt()
        return {'auth': True, '_id': data, 'is_admin': claims['is_admin']}, 200
