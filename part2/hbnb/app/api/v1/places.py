from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import jsonify, request


api = Namespace('places', description='Place operations')


amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        new_place = facade.create_place(place_data)
        if isinstance(new_place, str):
            return {"error": new_place}, 400

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner": new_place.owner.__dict__ if new_place.owner else None,
            "amenities": [amenity.__dict__ for amenity in new_place.amenities] if new_place.amenities else []
        }, 201
    
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        places = facade.get_all_places()
        return jsonify([{
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": place.owner.__dict__ if place.owner else None,
            "amenities": [amenity.__dict__ for amenity in place.amenities] if place.amenities else []
        }for place in places]), 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
        place = facade.get_place(place_id)
        if not place:
            return {"error", "Place not found"}, 404
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": place.owner.__dict__ if place.owner else None,
            "amenities": [amenity.__dict__ for amenity in place.amenities] if place.amenities else []
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            return {"error", "Place not found"}, 404
        return {
            "id": updated_place.id,
            "title": updated_place.title,
            "description": updated_place.description,
            "price": updated_place.price,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude,
            "owner": updated_place.owner.__dict__ if updated_place.owner else None,
            "amenities": [amenity.__dict__ for amenity in updated_place.amenities] if updated_place.amenities else []
        }, 200 
