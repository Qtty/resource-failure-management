import pymongo
from database.users import Users


class DB_Api():

    def __init__(self, host: str, user: str, password: str, is_initiated: bool) -> None:
        self.client = pymongo.MongoClient(f"mongodb://{host}:27017/")
        
        self.db = self.client["resource-management"]

    def users(self) -> Users:
        return Users(self.db)


db = DB_Api("172.17.0.2", "root", "root", False)