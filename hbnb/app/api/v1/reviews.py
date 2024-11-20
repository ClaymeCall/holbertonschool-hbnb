from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'text': fields.String(required=True, description='Text of the review'),
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new review"""

        current_user = get_jwt_identity()

        review_data = api.payload

        # Set   
        review_data["user_id"] = current_user["id"]

        try:
            place = facade.get_place(review_data["place_id"])

            if not place: 
                return {"error": "Place not found"}, 404
            
            if place.owner.id == current_user["id"]:
                return {"error": "You cannot review your own place"}, 400
            
            #if current_user has already reviewed the place

            existing_review = facade.get_review_by_place_and_user(
                review_data["place_id"], current_user["id"])
            
            if existing_review:
                return {"error": "You have already reviewed this place"}, 400

            new_review = facade.create_review(review_data)

        except ValueError as e:
            return {"error": str(e)}, 400
    
        return new_review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""

        review_list = facade.get_all_reviews()

        if review_list:
            return [review.to_dict() for review in review_list], 200

        return {"error": "No review found"}, 404


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400

        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get("is_admin", False)  

        try:
            existing_review = facade.get_review(review_id)

            if not existing_review:
                return {"error": "Review not found"}, 404
            
            if not is_admin and existing_review.user_id != current_user["id"]:
                return {"error": "Unauthorized action"}, 403
            
            review_data = api.payload
            update_review = facade.update_review(review_id, review_data)
            return {"message": "Review succesfully updated:",
                            "review": update_review.to_dict()}, 200

        except ValueError as e:
            return {"error": str(e)}, 400


    @api.response(200, 'Review deleted successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = current_user.get("is_admin", False)

        try:
            existing_review = facade.get_review(review_id)

            if not existing_review:
                return {"error": "'Review not found"}, 404

            if not is_admin and existing_review.user_id != current_user["id"]:
                return {"error": "Unauthorized action"}, 403

            if  facade.delete_review(review_id):
                return {"message": "Review deleted successfully"}, 200

        except ValueError as e:
            return {"error": str(e)}, 400

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200

        except ValueError as e:
            return {"error": str(e)}, 404
