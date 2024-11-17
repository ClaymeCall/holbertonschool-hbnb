from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.amenity import Amenity
from app.models.place import Place
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    #'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'token' : fields.String(required=True, description='Token of the owner'),
    #'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""

        current_user = get_jwt_identity()
        place_data = api.payload
        
        #if current_user id is same than owner_id
        if place_data.get("owner_id") and \
        place_data.get("owner_id") != current_user["id"]:
            return {"error": "You can only create a place for yourself"}, 403
        
        #set the owner_id with the current_user authenticated
        place_data["owner_id"] = current_user["id"]

        # Catching errors happening at Place instanciation
        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return new_place.to_dict(), 201

    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, 'No place found')
    def get(self):
        """Retrieve a list of all places"""

        place_list = facade.get_all_places()

        if place_list:
            return jsonify(place_list)

            # Base case if no places were found
        return {"error": "No place found"}, 404


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        return place.to_dict(), 200

    @api.expect(place_model, validate=False)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""

        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id != current_user["id"]:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload

        try:
            updated_place = facade.update_place(place_id, place_data)
        except ValueError as e:
            return {"error": str(e)}, 404

        return updated_place.to_dict(), 200

@api.route('/<place_id>/amenities')
class PlaceAmenity(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfuly added to place')
    @api.response(404, 'Not found')
    def post(self, place_id):
        """Add amenity to a place"""
        amenity_payload = api.payload

        try:
            facade.add_amenity_to_place(place_id, amenity_payload.get('name'))
        except ValueError as e:
            return {"error": str(e)}, 404

        return facade.place_repo.get(place_id).to_dict(), 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'List of review for the place retrieved successfully')
    @api.response(404, 'Not found')
    def get(self, place_id):
        """Retrieve a list of all places"""

        try:
            reviews = facade.get_reviews_by_place(place_id)
        except ValueError as e:
            return {"error": str(e)}, 404


        if reviews:
            return jsonify(reviews)

            # Base case if no reviews were found
        return {"error": "No reviews found for that place"}, 404
