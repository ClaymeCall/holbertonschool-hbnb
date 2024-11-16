from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace("users", description="User operations")

# Define the user model for input validation and documentation
user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True, description="First name of the user"
            ),
        "last_name": fields.String(
            required=True, description="Last name of the user"
            ),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)



@api.route("/")
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    def post(self):
        """Register a new user"""
        user_data = api.payload
        print("user payload recieved")

        # Catching errors happening at User instanciation
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return new_user.id, 201 

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self):
        """Retrieve a list of all users"""

        user_list = facade.get_all_users()

        # If there are users, return them as JSON
        if user_list:
            return jsonify(user_list)

        # Base case if no users were found
        return {"error": "No users found"}, 404

@api.route("/<user_id>")
class UserResource(Resource):
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")    
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if user:
            return user.to_dict(), 200
        
        return {"error": "User not found"}, 404



    @api.expect(user_model, validate=True)
    @api.response(204, "User details updated successfully")
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        user_data = api.payload

        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return updated_user.to_dict(), 204


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        return {'message': f'Hello, user {current_user["id"]}'}, 200