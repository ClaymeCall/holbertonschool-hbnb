from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from flask_restx import Namespace


api = Namespace("users", description="User operations")

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        # Checking email uniqueness
        existing_user = self.get_user_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError("Email already registered")

        # Create the new user and add it to the repo
        new_user = User(**user_data)
        self.user_repo.add(new_user)
        return new_user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        users = self.user_repo.get_all()
        return [user.__dict__ for user in users]

    def get_user_by_email(self, email):
        if not email:
            raise ValueError("Email cannot be empty.")
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        user_to_update = self.get_user(user_id)

        if not user_to_update:
            raise ValueError("User not found")

        # Checking email uniqueness
        existing_user = self.get_user_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError("Email already registered")

        self.user_repo.update(user_id, user_data)
        return user_to_update

    def create_amenity(self, amenity_data):
        # Checking amenity name uniqueness
        existing_amenity = self.amenity_repo.get_by_attribute('name', amenity_data.get('name'))
        if existing_amenity:
            raise ValueError("Amenity already registered")
        new_amenity = Amenity(**amenity_data)

        # Create the new amenity and add it to the repo
        self.amenity_repo.add(new_amenity)

        return new_amenity


    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity


    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass
    
    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        """Retrieves all places"""
        pass

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass
    
    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass


    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass
