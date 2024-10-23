from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Define the namespace
users_ns = Namespace('users', description='User related operations')

# Define the user model for input validation and documentation
user_model = users_ns.model('User', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

facade = HBnBFacade()

@users_ns.route('/')
class UserList(Resource):
    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        # Replace with actual user data retrieval logic
        return [{'id': 1, 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'}]

    @users_ns.doc('create_user')
    @users_ns.expect(user_model, validate=True)
    @users_ns.response(201, 'User successfully created')
    @users_ns.response(400, 'Email already registered')
    @users_ns.response(400, 'Invalid input data')
    @users_ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        user_data = users_ns.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return new_user, 201

@users_ns.route('/<int:user_id>')
class UserResource(Resource):
    @users_ns.response(200, 'User details retrieved successfully')
    @users_ns.response(404, 'User not found')
    @users_ns.marshal_with(user_model)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user, 200

    @users_ns.expect(user_model, validate=True)
    @users_ns.response(200, 'User details updated successfully')
    @users_ns.response(404, 'User not found')
    @users_ns.marshal_with(user_model)
    def put(self, user_id):
        """Update user details by ID"""
        user_data = users_ns.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        updated_user = facade.update_user(user_id, user_data)
        return updated_user, 200

