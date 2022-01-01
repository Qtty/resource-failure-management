import pymongo
from json import loads
from hashlib import sha256
from datetime import datetime
from os import environ


def hash_pwd(SALT: bytes, password: str) -> bytes:
        r = SALT + password
        return sha256(r.encode()).digest()

def insert_users(col, users: list):
    for i in users:
        col.insert_one(i)


while True:
    try:
        host = 'db'

        with open("config.json", "r") as f:
            config = loads(f.read())

        SALT = config["SALT"]
        client = pymongo.MongoClient(f"mongodb://{config['db']['username']}:{config['db']['password']}@{host}:27017/")
        db = client['resource-management']
        users_col = db['users']

        config['admin']['password'] = hash_pwd(SALT, config['admin']['password'])
        config['admin']['date'] = datetime.utcnow()
        insert_users(users_col, [config['admin']])

        break
    except Exception:
        pass
