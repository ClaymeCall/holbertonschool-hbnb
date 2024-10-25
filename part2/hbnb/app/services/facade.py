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
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        amenities = self.amenity_repo.get_all()
        for amenity in amenities:
            for key, value in amenity.__dict__.items():
                if isinstance(value, list):
                    amenity.__dict__[key] = value
        return amenities

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = self.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity


    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        """ Create new place from place data,
        take a dict of place data, validate owner, retrieves associated amenities
        and add the new plac to the repo"""
        try:
            place = Place(**place_data)
            owner = self.get_user(place.owner_id)
            if not owner:
                raise ValueError("Owner not found")
            
            amenity_ids = place_data.get("amenities", [])

            place.amenities = []
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                place.amenities.append(amenity)
        
            self.place_repo.add(place)
            return place
        except ValueError as e:
            return str(e)
    

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        """retrieves the place by id"""
        place = self.place_repo.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        
        place.owner = self.get_user(place.owner_id)
        place.amenities = [self.get_amenity(amenity_id) for amenity_id in place.amenities]
        return place

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        """Retrieves all places"""
        places = self.place_repo.get_all()
        for place in places:
            place.owner = self.get_user(place.owner_id)
            place.amenities = [self.get_amenity(amenity_id) for amenity_id in place.amenities]
        return places

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        """Retrieve a place by id to update it"""
        place = self.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)
    

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
