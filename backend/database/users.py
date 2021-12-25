from hashlib import sha256
from datetime import datetime
from os import getenv
from bson.json_util import dumps


class Users():

    def __init__(self, db) -> None:
        self.users = db['users']
        self.SALT = getenv("SALT")

    def get_user(self, mail: str, password: str) -> dict:
        res = self.users.find_one({
            "mail": mail,
            "password": self.hash_pwd(password)
        })

        if res:
            return res
        return None

    def insert_user(self, mail: str, password: str, is_admin: str = False) -> None:
        self.users.insert_one({
            "mail": mail,
            "password": self.hash_pwd(password),
            "is_admin": is_admin,
            "date": datetime.utcnow()
        })

    def hash_pwd(self, password: str) -> bytes:
        r = self.SALT + password
        return sha256(r.encode()).digest()
