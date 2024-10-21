from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

# Define the models for related entities
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

# Define the place model for input validation and documentation
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
        data = request.json
        try:
            new_place = facade.create_place(data)
            return new_place, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place_by_id(place_id)
        if place:
            return place, 200
        else:
            api.abort(404, 'Place not found')

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = request.json
        try:
            updated_place = facade.update_place(place_id, data)
            if updated_place:
                return updated_place, 200
            else:
                api.abort(404, 'Place not found')
        except ValueError as e:
            api.abort(400, str(e))

# Review place model
review_model = api.model('Review', {
    'user_id': fields.String(required=True, description='The user identifier'),
    'text': fields.String(required=True, description='The review text'),
    'rating': fields.Integer(required=True, description='The review rating')
})

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    def post(self, place_id):
        """Create a new review for a place"""
        data = request.json
        try:
            new_review = facade.create_review(place_id, data)
            return new_review, 201
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError:
            api.abort(404, 'Place not found')

    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve a list of all reviews for a place"""
        reviews = facade.get_reviews_by_place_id(place_id)
        if reviews is not None:
            return reviews, 200
        else:
            api.abort(404, 'Place not found')

@api.route('/<place_id>/reviews/<review_id>')
class PlaceReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, place_id, review_id):
        """Get review details by ID"""
        review = facade.get_review_by_id(place_id, review_id)
        if review:
            return review, 200
        else:
            api.abort(404, 'Review not found')

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id, review_id):
        """Update a review's information"""
        data = request.json
        try:
            updated_review = facade.update_review(place_id, review_id, data)
            if updated_review:
                return updated_review, 200
            else:
                api.abort(404, 'Review not found')
        except ValueError as e:
            api.abort(400, str(e))
