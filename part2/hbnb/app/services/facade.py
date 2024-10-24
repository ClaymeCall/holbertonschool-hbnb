from app.persistence.repository import InMemoryRepository

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
        """
        Create a new amenity.

        :param amenity_data: Dictionary containing amenity details.
        :return: Dictionary containing the created amenity with its ID.
        """
        amenity_id = self.next_id
        self.next_id += 1
        amenity_data['id'] = amenity_id
        self.amenities[amenity_id] = amenity_data
        return amenity_data

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by its ID.

        :param amenity_id: ID of the amenity to retrieve.
        :return: Dictionary containing the amenity details, or None if not found.
        """
        return self.amenities.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all amenities.

        :return: List of dictionaries containing all amenities.
        """
        return list(self.amenities.values())

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity.

        :param amenity_id: ID of the amenity to update.
        :param amenity_data: Dictionary containing updated amenity details.
        :return: Dictionary containing the updated amenity, or None if not found.
        """
        if amenity_id in self.amenities:
            self.amenities[amenity_id].update(amenity_data)
            return self.amenities[amenity_id]
        return None

# Example usage:
amenity_service = AmenityService()

# Create a new amenity
new_amenity = amenity_service.create_amenity({'name': 'WiFi', 'description': 'High-speed internet'})
print(new_amenity)

# Retrieve an amenity by ID
retrieved_amenity = amenity_service.get_amenity(new_amenity['id'])
print(retrieved_amenity)

# Retrieve all amenities
all_amenities = amenity_service.get_all_amenities()
print(all_amenities)

# Update an amenity
updated_amenity = amenity_service.update_amenity(new_amenity['id'], {'description': 'Free high-speed internet'})
print(updated_amenity)

class AirbnbClone:
    def __init__(self):
        self.places = {}

    def create_place(self, place_data):
        """
        Create a new place with the given data.
        :param place_data: Dictionary containing place details.
        """
        # Validate place data
        if not self._validate_place_data(place_data):
            raise ValueError("Invalid place data")

        place_id = len(self.places) + 1
        self.places[place_id] = place_data
        return place_id

    def get_place(self, place_id):
        """
        Retrieve a place by its ID.
        :param place_id: ID of the place to retrieve.
        :return: Dictionary containing place details.
        """
        place = self.places.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        """
        Retrieve all places.
        :return: List of dictionaries containing place details.
        """
        return list(self.places.values())

def update_place(self, place_id, place_data):
    """
    Update a place with the given data.
    :param place_id: ID of the place to update.
    :param place_data: Dictionary containing updated place details.
    """
    if place_id not in self.places:
        raise ValueError(f"Place with ID {place_id} not found")

    # Validate place data
    if not self._validate_place_data(place_data):
        raise ValueError("Invalid place data")

    self.places[place_id].update(place_data)

def _validate_place_data(self, place_data):
    """
    Validate the place data.
    :param place_data: Dictionary containing place details.
    :return: Boolean indicating if the data is valid.
    """
    required_fields = ['name', 'price', 'latitude', 'longitude', 'owner', 'amenities']
    for field in required_fields:
        if field not in place_data:
            print(f"Missing required field: {field}")
            return False

    if not (isinstance(place_data['price'], (int, float)) and place_data['price'] >= 0):
        print("Invalid price")
        return False

    if not (-90 <= place_data['latitude'] <= 90):
        print("Invalid latitude")
        return False

    if not (-180 <= place_data['longitude'] <= 180):
        print("Invalid longitude")
        return False

    # Additional validations for owner and amenities can be added here
    if not isinstance(place_data['owner'], str):
        print("Invalid owner")
        return False

    if not isinstance(place_data['amenities'], list):
        print("Invalid amenities")
        return False

    return True

# Example usage:
airbnb = AirbnbClone()

# Create a new place
place_id = airbnb.create_place({
    'name': 'Cozy Apartment',
    'price': 100,
    'latitude': 37.7749,
    'longitude': -122.4194,
    'owner': 'John Doe',
    'amenities': ['WiFi', 'Kitchen', 'Parking']
})

# Retrieve the created place
place = airbnb.get_place(place_id)
print(place)

# Update the place
airbnb.update_place(place_id, {
    'price': 120,
    'amenities': ['WiFi', 'Kitchen', 'Parking', 'Pool']
})

# Retrieve all places
all_places = airbnb.get_all_places()
print(all_places)

class ReviewService:
    def __init__(self, db):
        self.db = db

    def create_review(self, review_data):
        # Validate input data
        if not all(key in review_data for key in ('user_id', 'place_id', 'rating', 'comment')):
            raise ValueError("Missing required fields in review_data")

        user_id = review_data['user_id']
        place_id = review_data['place_id']
        rating = review_data['rating']
        comment = review_data['comment']

        # Validate rating
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        # Placeholder for actual database insertion logic
        review_id = self.db.insert_review(user_id, place_id, rating, comment)

        return review_id

    def get_review(self, review_id):
        # Placeholder for actual database retrieval logic
        review = self.db.get_review_by_id(review_id)

        if not review:
            raise ValueError("Review not found")

        return review

    def get_all_reviews(self):
        # Placeholder for actual database retrieval logic
        reviews = self.db.get_all_reviews()
        return reviews

    def get_reviews_by_place(self, place_id):
        # Placeholder for actual database retrieval logic
        reviews = self.db.get_reviews_by_place_id(place_id)
        return reviews

    def update_review(self, review_id, review_data):
        # Validate input data
        if not any(key in review_data for key in ('rating', 'comment')):
            raise ValueError("No fields to update in review_data")

        # Placeholder for actual database update logic
        updated = self.db.update_review(review_id, review_data)

        if not updated:
            raise ValueError("Review not found or update failed")

        return updated

    def delete_review(self, review_id):
        # Placeholder for actual database deletion logic
        deleted = self.db.delete_review(review_id)

        if not deleted:
            raise ValueError("Review not found or deletion failed")

        return deleted

# Example usage:
# db = Database()  # Assuming you have a Database class that handles the actual DB operations
# review_service = ReviewService(db)
# review_data = {
#     'user_id': 1,
#     'place_id': 101,
#     'rating': 4,
#     'comment': 'Great place!'
# }
# review_id = review_service.create_review(review_data)
# print(review_id)

