from flask import Flask
from flask_restful import Api
from login import Login

app = Flask(__name__)
api = Api(app)

api.add_resource(Login, "/api/login")


if __name__ == "__main__":
    app.run(debug=True)
