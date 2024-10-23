from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade



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


@api.route("/", methods=['POST'])
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if not user_data:
            return {"error": "invalid input data. json required"}, 400

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


@api.route("/", methods=['GET'])
class UserList(Resource):
    @api.response(200, "list of users retrieved is a success")
    @api.response(404, "user not found")
    def get(self):
        """retrieve users list"""
        users_list = [user.__dict__ for user in facade.get_all_users()]
        return users_list


@api.route("/<user_id>", methods=['GET'])
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

@api.route("/<user_id>", methods=['PUT'])
class UserResource(Resource):
    @api.response(200, "User details updating successfully")
    @api.response(404, "User not found")
    @api.response(400, "Invalid input data")
    def put(self, user_id):
        """Update user details by ID"""

        user_data = api.payload
        if not user_data:
            return {"error": "Invalid input data"}, 400

        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {"error": "user not found"}, 404
        
        updated_user = [user.__dict__ for user in facade.update_user()]
        return updated_user
