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

        # Catching errors happening at User instanciation
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return new_user.to_dict()            

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
        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200


    @api.expect(user_model, validate=True)
    def put(self, user_id):
        user_data = api.payload

        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return updated_user.to_dict(), 200
