import pymongo
from database.resources import Resources
from database.users import Users
from database.tickets import Tickets
from json import loads


class DB_Api():

    def __init__(self, host: str, user: str, password: str) -> None:
        self.client = pymongo.MongoClient(f"mongodb://{user}:{password}@{host}:27017/")
        
        self.db = self.client["resource-management"]

    def users(self) -> Users:
        return Users(self.db)

    def resources(self) -> Resources:
        return Resources(self.db)

    def tickets(self) -> Tickets:
        return Tickets(self.db)

with open("config.json", "r") as f:
    config = loads(f.read())

db = DB_Api("db", config['db']['username'], config['db']['password'])