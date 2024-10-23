# app/api/v1/__init__.py
from flask_restx import Api
from flask import Blueprint
from app.api.v1.users import users_ns

# Create a Blueprint for the API
api_blueprint = Blueprint('api', __name__)

# Initialize the API
api = Api(api_blueprint, version='1.0', title='My API', description='A simple API')

# Register the users namespace
api.add_namespace(users_ns, path='/users')

# Register the blueprint with the app
def init_app(app):
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

