from flask_restx import Namespace, Resource, fields
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

        # Check uniqueness of input email in persistance layer
        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400

        new_user = facade.create_user(user_data)
        return {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
        }, 201
    

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self):
        users_list = [user.__dict__ for user in facade.get_all_users()]
        if not users_list:
            return {"No users found"}, 404        
        return jsonify(users_list)


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

    def put(self, user_id):
        user_data = api.payload
        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        facade.user_repo.update(user_id, user_data)
        return user_data
