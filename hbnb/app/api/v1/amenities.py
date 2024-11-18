from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("amenities", description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model(
    'Amenity',
    {'name': fields.String(required=True, description='Name of the amenity')},
)


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        # Catching errors happening at Amenity instanciation
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return new_amenity.to_dict(), 201

    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, "No amenities found")
    def get(self):
        """Retrieve a list of all amenities"""

        amenity_list = facade.get_all_amenities()

        # If there are amenities, return them as JSON
        if amenity_list:
            return amenity_list

        # Base case if no amenities were found
        return {"message": "No amenities found"}, 404


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        amenity_data = api.payload
        """update an amenity data by id"""

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return updated_amenity.to_dict(), 200
"""
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Not allowed you are not the owner of this place')
    def delete(self, amenity_id):
        ""delete amenity by id if user is the owner of amenity's place""

        try:
            current_user = facade.get_current_user()
            facade.delete_amenity(amenity_id, current_user)

        except ValueError as e:
            return {"error": str(e)}, 404

        except ValueError as e:
            return {"error": str(e)}, 403

        return {"message": "Amenity deleted successfully"}, 200
"""
