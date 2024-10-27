from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import jsonify

api = Namespace("amenities", description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model(
    'Amenity',
    {
    'name': fields.String(required=True, description='Name of the amenity')
    },
)

facade = HBnBFacade()

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

        return new_amenity.to_dict()            

    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, "No amenities found")
    def get(self):
        """Retrieve a list of all amenities"""

        amenities_list = facade.get_all_amenities()

        if not amenities_list:
            return {"message": "No amenities found"}, 404

        return jsonify([amenity.__dict__ for amenity in amenities_list])

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {
            "id": amenity.id,
            "name": amenity.name,
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        if not amenity_data or not amenity_data.get("name"):
            return {"error": "Invalid input data"}, 400
        
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {"error": "Amenity not found"}, 404
        return {
            "id": updated_amenity.id,
            "name": updated_amenity.name
            }, 200
