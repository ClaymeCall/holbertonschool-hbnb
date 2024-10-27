from flask_restx import Namespace, Resource, fields
from app.models import user
from app.services.facade import HBnBFacade
from flask import jsonify

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
    },
)

facade = HBnBFacade()


@api.route("/")
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if not user_data:
            return {"error": "invalid input data. json required"}, 400

        existing_user = facade.get_user_by_email(user_data.get("email"))
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
        }, 201
    

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self):
        """Retrieve a list of all users"""

        users_list = facade.get_all_users()

        user_data_list = []
        
        """Check that user is a dictionary with the correct keys"""
        for user in users_list:
            if isinstance(user, dict):
                if 'id' in user:
                    if 'first_name' in user:
                        if 'last_name' in user:
                            if 'email' in user:
                                user_data_list.append(user)

        if user_data_list:
            return jsonify(user_data_list)
        else:
            return {"error": "No users found"}, 404


@api.route("/<user_id>")
class UserResource(Resource):
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")    
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 200

    @api.expect(user_model, validate=True)
    def put(self, user_id):
        user_data = api.payload
        user_to_update = facade.get_user(user_id)

        if not user_to_update:
            return {"error": "User not found"}, 404

        facade.user_repo.update(user_id, user_data)
        return user_data
