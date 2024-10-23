from flask_restx import Namespace, Resource, fields, reqparse
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

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
        data = api.payload
        name = data.get('name')
        if not name:
            api.abort(400, 'Invalid input data')
        # Placeholder for the logic to register a new amenity
        # For example:
        # new_amenity = facade.create_amenity(name)
        return {'message': 'Amenity successfully created'}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Placeholder for logic to return a list of all amenities
        # For example:
        # amenities = facade.get_all_amenities()
        return {'amenities': []}, 200

@api.route('/<int:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Placeholder for the logic to retrieve an amenity by ID
        # For example:
        # amenity = facade.get_amenity_by_id(amenity_id)
        # if not amenity:
        #     api.abort(404, 'Amenity not found')
        return {'amenity': {}}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload
        name = data.get('name')
        if not name:
            api.abort(400, 'Invalid input data')
        # Placeholder for the logic to update an amenity by ID
        # For example:
        # updated_amenity = facade.update_amenity(amenity_id, name)
        # if not updated_amenity:
        #     api.abort(404, 'Amenity not found')
        return {'message': 'Amenity updated successfully'}, 200

