from flask import Flask
from flask import send_from_directory
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from login import Login
from admin import Admin
from resources import Resources
from responsable import Responsable
from tickets import Tickets
from os import urandom, environ
from populate import init


app = Flask(__name__)
cors = CORS(app)
jwt = JWTManager(app)
api = Api(app)

SALT = "U!'\xcd\xe0c^+\xb1V\x97\x8f\x02{\xbd\xfb"
environ["SALT"] = SALT
app.config["JWT_SECRET_KEY"] = "yellow submarine"
app.config["PROPAGATE_EXCEPTIONS"] = True


@app.route('/api/qrcodes/<path:path>')
def send_img(path):
    return send_from_directory('qrcodes', path)

api.add_resource(Login, "/api/login")
api.add_resource(Admin, "/api/admin")
api.add_resource(Resources, "/api/resources")
api.add_resource(Responsable, "/api/responsable")
api.add_resource(Tickets, '/api/tickets')

init()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
