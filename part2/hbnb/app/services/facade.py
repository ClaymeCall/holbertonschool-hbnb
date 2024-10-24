from app.persistence.repository import InMemoryRepository
import logging

# Assuming User class is defined or imported
class User:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

class AmenityService:
    def __init__(self):
        self.amenities = {}
        self.next_id = 1

    def create_amenity(self, amenity_data):
        amenity_id = self.next_id
        self.next_id += 1
        amenity_data['id'] = amenity_id
        self.amenities[amenity_id] = amenity_data
        return amenity_data

    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)

    def get_all_amenities(self):
        return list(self.amenities.values())

    def update_amenity(self, amenity_id, amenity_data):
        if amenity_id in self.amenities:
            self.amenities[amenity_id].update(amenity_data)
            return self.amenities[amenity_id]
        return None

class AirbnbClone:
    def __init__(self):
        self.places = {}
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

    def create_place(self, place_data):
        if not self._validate_place_data(place_data):
            raise ValueError("Invalid place data")

        place_id = len(self.places) + 1
        self.places[place_id] = place_data
        return place_id

    def get_place(self, place_id):
        place = self.places.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        return list(self.places.values())

    def update_place(self, place_id, place_data):
        if place_id not in self.places:
            raise ValueError(f"Place with ID {place_id} not found")

        if not self._validate_place_data(place_data):
            raise ValueError("Invalid place data")

        self.places[place_id].update(place_data)

    def _validate_place_data(self, place_data):
        required_fields = ['name', 'price', 'latitude', 'longitude', 'owner', 'amenities']
        for field in required_fields:
            if field not in place_data:
                self.logger.error(f"Missing required field: {field}")
                return False

        if not (isinstance(place_data['price'], (int, float)) and place_data['price'] >= 0):
            self.logger.error("Invalid price")
            return False

        if not (-90 <= place_data['latitude'] <= 90):
            self.logger.error("Invalid latitude")
            return False

        if not (-180 <= place_data['longitude'] <= 180):
            self.logger.error("Invalid longitude")
            return False

        if not isinstance(place_data['owner'], str):
            self.logger.error("Invalid owner")
            return False

        if not isinstance(place_data['amenities'], list):
            self.logger.error("Invalid amenities")
            return False

        for amenity in place_data['amenities']:
            if not isinstance(amenity, str):
                self.logger.error(f"Invalid amenity: {amenity}")
                return False

        return True
    def __init__(self, db):
        self.db = db

    def create_review(self, review_data):
        if not all(key in review_data for key in ('user_id', 'place_id', 'rating', 'comment')):
            raise ValueError("Missing required fields in review_data")

        user_id = review_data['user_id']
        place_id = review_data['place_id']
        rating = review_data['rating']
        comment = review_data['comment']

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review_id = self.db.insert_review(user_id, place_id, rating, comment)
        return review_id

    def get_review(self, review_id):
        review = self.db.get_review_by_id(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        reviews = self.db.get_all_reviews()
        return reviews

    def get_reviews_by_place(self, place_id):
        reviews = self.db.get_reviews_by_place_id(place_id)
        return reviews

    def update_review(self, review_id, review_data):
        if not any(key in review_data for key in ('rating', 'comment')):
            raise ValueError("No fields to update in review_data")

        updated = self.db.update_review(review_id, review_data)
        if not updated:
            raise ValueError("Review not found or update failed")
        return updated

    def delete_review(self, review_id):
        deleted = self.db.delete_review(review_id)
        if not deleted:
            raise ValueError("Review not found or deletion failed")
        return deleted

