from flask import Flask
from flask_restx import Api
from app.api.v1.users import users_ns

def create_app():
    app = Flask(__name__)

    api = Api(app, version='1.0', title='My API', description='A simple API')

    api.add_namespace(users_ns, path='/api/v1/users')

    return app
