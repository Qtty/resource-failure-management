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


SALT = "U!'\xcd\xe0c^+\xb1V\x97\x8f\x02{\xbd\xfb"
host = '172.17.0.2'
client = pymongo.MongoClient(f"mongodb://{host}:27017/")
db = client['resource-management']
users_col = db['users']

users = []
for i in range(20):
    r = get('https://randomuser.me/api/?inc=name,email,login')
    res = r.json()
    users.append({
        'nom': res['results'][0]['name']['last'],
        'prenom': res['results'][0]['name']['first'],
        'mail': res['results'][0]['email'],
        'password': hash_pwd(SALT, res['results'][0]['login']['password']),
        'is_admin': False,
        'is_resp': True,
        'date': datetime.utcnow()
    })

insert_users(users_col, users)
for i in users_col.find({}):
    print(i)