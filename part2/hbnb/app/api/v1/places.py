from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import jsonify

api = Namespace("places", description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model(
        'Place',
        {
            'name':fields.String(required=True, description='Name of the place'),
            'description':fields.String(required=True, description='Description of the place'),
            'price_per_night':fields.Float(required=True, description='Price per night'),
            'number_of_rooms':fields.Integer(required=True, description='Number of rooms'),
            'number_of_bathrooms':fields.Integer(required=True, description='Number of bathrooms'),
            'max_guest':fields.Integer(required=True, description='Maximum number of guests'),
            'amenities':fields.List(fields.String, description='List of amenities')
            },
        )

facade = HBnBfacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.playload

    if not place_data:
        return {"error": "Invalid input data. JSON required"}, 400

    new_place = facade.create_place(place_data)
    return {
            "id": new_place.id,
            "name": new_place.name,
            "description": new_place.description,
            "price_per_night": new_place.price_per_night,
            "number_of_rooms": new_place.number_of_rooms,
            "number_of_bathrooms": new_place.number_of_bathrooms,
            "max_guest": new_place.max_guest,
            "amenities": new_place.amenities
            }, 201

    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, "No places found")
    def get(self):
        """Retrieve a list of all places"""
        places_list = facade.get_all_places()

        if not places_list:
            return {"message": "No places found"}, 404

        return jsonify([place.__dict__ for place in places_list])

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
             return {"error": "Place not found"}, 404
        return {
                 "id": place.id,
                 "name": place.name,
                 "description": place.description,
                 "price_per_night": place.price_per_night,
                 "number_of_rooms": place.number_of_rooms,
                 "number_of_bathrooms": place.number_of_bathrooms,
                 "max_guest": place.max_guest,
                 "amenities": place.amenities
                 }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        if not place_data or not place_data.get("name"):
            return {"error": "Invalid input data"}, 400

        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            return {"error": "Place not found"}, 404
        return {
                "id": updated_place.id,
                "name": updated_place.name,
                "description": updated_place.description,
                "price_per_night": updated_place.price_per_night,
                "number_of_rooms": updated_place.number_of_rooms,
                "number_of_bathrooms": updated_place.number_of_bathrooms,
                "max_guest": updated_place.max_guest,
                "amenities": updated_place.amenities
                }, 200

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        deleted = facade.delete_place(place_id)
        if not deleted:
            return {"error": "Place not found"}, 404
        return {"message": "Place deleted successfully"}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return jsonify([review.__dict__ for review in reviews])
