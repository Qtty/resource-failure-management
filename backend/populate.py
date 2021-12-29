from hashlib import sha256
from datetime import datetime
from requests import get
import pymongo


def hash_pwd(SALT: str, password: str) -> bytes:
        r = SALT + password
        return sha256(r.encode()).digest()

def insert_users(col, users: list):
    for i in users:
        col.insert_one(i)

def init():
    SALT = "U!'\xcd\xe0c^+\xb1V\x97\x8f\x02{\xbd\xfb"
    host = 'db'
    client = pymongo.MongoClient(f"mongodb://{host}:27017/")
    db = client['resource-management']
    users_col = db['users']

    users = [{
        "nom": "RUSKI",
        "prenom": "Bratan",
        "mail": "admin@univ.fr",
        "password": hash_pwd(SALT, "admin"),
        "is_admin": True,
        "is_resp": False,
        "date": datetime.utcnow()
    }]

    insert_users(users_col, users)
