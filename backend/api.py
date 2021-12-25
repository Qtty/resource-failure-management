from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from login import Login
from admin import Admin
from os import urandom, environ


app = Flask(__name__)
cors = CORS(app)
jwt = JWTManager(app)
api = Api(app)

SALT = "U!'\xcd\xe0c^+\xb1V\x97\x8f\x02{\xbd\xfb"
environ["SALT"] = SALT
app.config["JWT_SECRET_KEY"] = "yellow submarine"

api.add_resource(Login, "/api/login")
api.add_resource(Admin, "/api/admin")


if __name__ == "__main__":
    app.run(debug=True)
