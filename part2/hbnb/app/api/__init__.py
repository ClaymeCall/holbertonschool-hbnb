from flask import Blueprint
from flask_restx import Api

# Import namespaces
from .v1.users import api as users_ns
from .v1.places import api as places_ns
from .v1.amenities import api as amenities_ns
from .v1.reviews import api as reviews_ns

# Create a Blueprint for the API
api_bp = Blueprint('api', __name__)

# Initialize the API
api = Api(api_bp, title='Airbnb Clone API', version='1.0', description='API for Airbnb Clone Project')

# Register the namespaces
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(reviews_ns, path='/reviews')

# Register the Blueprint
def create_app(app):
    app.register_blueprint(api_bp, url_prefix='/api')

