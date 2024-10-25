from flask import Flask
from flask_restx import Api
from app.api.v1.places import api as places_api

def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Add the namespace to the API
    api.add_namespace(places_api, path='/api')

    return app

