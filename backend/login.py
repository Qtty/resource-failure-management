from flask import request
from flask_restful import Resource
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
            return result, 200

        return {"auth": False}, 403
