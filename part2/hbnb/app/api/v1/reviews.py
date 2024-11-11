from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask import jsonify

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'text': fields.String(required=True, description='Text of the review'),
    'user_id': fields.String(required=True, description='ID of the user'),
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload

        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {"error": str(e)}, 400
    
        return new_review.to_dict()

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""

        review_list = facade.get_all_reviews()

        if review_list:
            return jsonify(review_list)

        return {"error": "No review found"}, 404


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = review.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400

        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        
        review_data = api.payload

        try:
            existing_review = facade.get_review(review_id)
            if not existing_review:
                return {"error": "Review not found"}, 404
            
            update_review = facade.update_review(review_id, review_data)
            return jsonify({"message": "Review succesfully updated:",
                            "review": update_review.to_dict()}), 200

        except ValueError as e:
            return {"error": str(e)}, 400


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            result = facade.delete_review(review_id)
            if result:
                return {"message": "Successful deleting review"}, 200
        except ValueError as e:
            return {"error": str(e)}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""

        try:
            reviews = facade.get_reviews_by_place(place_id)
            return jsonify([review.to_dict() for review in reviews]), 200

        except ValueError as e:
            return {"error": str(e)}, 404