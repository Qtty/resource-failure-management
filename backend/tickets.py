from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from utility import check_args
from database.db_api import db
from responsable import check_if_resp
from responsable import check_if_resp_decorator


class Tickets(Resource):

    put_args = [
        'desc',
        'res_id'
    ]

    delete_args = [
        '_id'
    ]

    def get(self):
        data = dict(request.args)

        if 'resp_id' not in data and 'res_id' not in data:
            return 'Missing Arguments', 400

        if 'resp_id' in data:
            if not check_if_resp():
                return 'Pas autoriser', 401

            kwargs = {'resp_id': get_jwt_identity()}

        elif 'res_id' in data:
            kwargs = {'res_id': data['res_id']}

        return db.tickets().get_tickets(**kwargs)

    def put(self):
        if not check_args(request.get_json(), *self.put_args):
            return "Missing Arguments", 400

        data = request.get_json()

        res = db.resources().get_resource(_id=data['res_id'], include_resp=True)
        if not res:
            return "Resource n'existe pas", 404

        name = None if 'nom' not in data else data['nom']
        ticket = db.tickets().add_ticket(res_id=data['res_id'], resp_id=res['resp_id'], desc=data['desc'], name=name)

        if ticket:
            return ticket, 200

        return '', 500

    @check_if_resp_decorator
    def delete(self):
        if not check_args(request.get_json(), *self.delete_args):
            return "Missing Arguments", 400

        data = request.get_json()

        if not db.tickets().get_ticket(data['_id'], get_jwt_identity()):
            return 'Pas autoriser pour cette ticket', 401

        res = db.tickets().delete_ticket(data['_id'])

        return '', 200