from flask import Flask, render_template
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import os

# Instances
bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()

# Namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {your_token}"'
        }
    }


def create_app(config_class="config.DevelopmentConfig"):

    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), 'static'),
        template_folder=os.path.join(os.path.dirname(__file__), 'web_client')
    )

    app.config.from_object(config_class)

    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'your_secret_key_here')

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        security='Bearer Auth',
        doc='/api/v1/doc',
        prefix='/api/v1',
        authorizations=authorizations
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    # Routes for HTML pages
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/<page_name>.html')
    def render_page(page_name):
        try:
            return render_template(f'{page_name}.html')
        except Exception as e:
            return render_template('404.html'), 404
    
    return app
