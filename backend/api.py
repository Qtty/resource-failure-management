from flask import Flask
from flask_restful import Api
from login import Login
from os import urandom, environ


SALT = "U!'\xcd\xe0c^+\xb1V\x97\x8f\x02{\xbd\xfb"
environ["SALT"] = SALT

app = Flask(__name__)
api = Api(app)

api.add_resource(Login, "/api/login")


if __name__ == "__main__":
    app.run(debug=True)
