from datetime import date, datetime
from bson.objectid import ObjectId


class Tickets():

    def __init__(self, db) -> None:
        self.tickets = db['tickets']

    def get_ticket(self, _id: str, resp_id: str) -> dict:
        try:
            res = self.tickets.find_one({
                '_id': ObjectId(_id),
                'resp_id': ObjectId(resp_id)
            })

            if res:
                res = {
                    '_id': res['_id'].binary.hex(),
                    'description': res['description'],
                    'resource_id': res['resource_id'].binary.hex(),
                    'name': res['name'],
                    'date': res['date'].strftime("%Y/%m/%d %H:%M:%S")
                }

                return res
        except Exception:
            return None

        return None

    def get_tickets(self, resp_id: str = None, res_id: str = None) -> list:
        try:
            if resp_id:
                res = self.tickets.find({
                    'resp_id': ObjectId(resp_id)
                })
            elif res_id:
                res = self.tickets.find({
                    'resource_id': ObjectId(res_id)
                })
            else:
                return None

            if res:
                res = [{
                    '_id': i['_id'].binary.hex(),
                    'description': i['description'],
                    'resource_id': i['resource_id'].binary.hex(),
                    'name': i['name'],
                    'date': i['date'].strftime("%Y/%m/%d %H:%M:%S")
                } for i in res]

                return res
        except Exception:
            return None

        return None

    def add_ticket(self, res_id: str, resp_id: str, desc: str, name: str = None) -> str:
        if not name:
            name = "Anonyme"

        res = self.tickets.insert_one({
            'description': desc,
            'resource_id': ObjectId(res_id),
            'resp_id': ObjectId(resp_id),
            'name': name,
            'date': datetime.utcnow()
        })

        return res.inserted_id.binary.hex()

    def delete_ticket(self, _id: str) -> dict:
        return self.tickets.delete_one({
            '_id': ObjectId(_id)
        })