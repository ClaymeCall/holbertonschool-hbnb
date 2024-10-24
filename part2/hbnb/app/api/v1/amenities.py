from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
import json

api = Namespace("amenities", description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        if not amenity_data or not amenity_data.get("name"):
            return {"error": "Invalid input data"}, 400
        
        new_amenity = facade.create_amenity(amenity_data)
        return {
            "id": new_amenity.id,
            "name": new_amenity.name,
            "created_at": new_amenity.created_at.isoformat(),
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')

    def get(self):
        """Retrieve a list of all amenities"""
        print("t", facade.get_all_amenities())
        amenities_list = [[amenity.__dict__ for amenity in facade.get_all_amenities()]]
       
        print(amenities_list)
        return json.dumps(amenities_list), 200


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
            "name": amenity.name
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
