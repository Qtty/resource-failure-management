from datetime import datetime
from bson.objectid import ObjectId


class Resources():

    def __init__(self, db) -> None:
        self.resources = db['resources']

    def get_resource(self, _id: str, resp_id: str = None, include_resp: bool = False) -> dict:
        try:
            if not resp_id:
                res = self.resources.find_one({
                    '_id': ObjectId(_id)
                })
            else:
                res = self.resources.find_one({
                    '_id': ObjectId(_id),
                    'resp_id': ObjectId(resp_id)
                })

            if res:
                resource = {
                    '_id': res['_id'].binary.hex(),
                    'description': res['description'],
                    'localisation': res['localisation']
                }

                if include_resp:
                    resource['resp_id'] = res['resp_id'].binary.hex()

                return resource
        except Exception:
            return None

        return None

    def get_resources(self, resp_id: str) -> list:
        res = self.resources.find({
            'resp_id': ObjectId(resp_id)
        })

        if res:
            res = [{
                '_id': i['_id'].binary.hex(),
                'description': i['description'],
                'localisation': i['localisation']
            } for i in res]

            return res

        return None

    def add_resource(self, desc: str, loc: str, resp_id: str) -> str:
        res = self.resources.insert_one({
            'description': desc,
            'localisation': loc,
            'resp_id': ObjectId(resp_id),
            'date': datetime.utcnow()
        })

        return res.inserted_id.binary.hex()

    def delete_resource(self, _id: str) -> None:
        self.resources.delete_one({
            '_id': ObjectId(_id)
        })