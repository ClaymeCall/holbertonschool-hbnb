from app.persistence.repository import InMemoryRepository
from app.models.user import User

class InMemoryRepository:
    def __init__(self):
        self.data = {}

    def add(self, item):
        self.data[item['id']] = item

    def get(self, item_id):
        return self.data.get(item_id)

    def update(self, item_id, item_data):
        if item_id in self.data:
            self.data[item_id].update(item_data)
        else:
            raise ValueError(f"Item with ID {item_id} not found")

    def delete(self, item_id):
        if item_id in self.data:
            del self.data[item_id]
        else:
            raise ValueError(f"Item with ID {item_id} not found")

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
<<<<<<< HEAD
        # Validate user data
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")

        # Assign a unique ID to the new user
        user_id = len(self.user_repo.data) + 1
        user_data['id'] = user_id

        # Add the new user to the repository
        self.user_repo.add(user_data)
        return user_data

    def get_place(self, place_id):
        # Fetch the place by ID from the repository
        place = self.place_repo.get(place_id)
        if place is None:
            raise ValueError(f"Place with ID {place_id} not found")
        return place

class PlaceManager:
    def __init__(self):
        self.places = {}
        self.next_id = 1
=======
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass
>>>>>>> d1d0ebd96edd01586f5e2001e6196d4116b38318

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass


<<<<<<< HEAD
    def _validate_place_data(self, place_data):
        required_fields = ['name', 'price', 'latitude', 'longitude']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"Missing required field: {field}")

        self.validate_price(place_data['price'])
        self.validate_coordinates(place_data['latitude'], place_data['longitude'])

    def create_place(self, place_data):
        self._validate_place_data(place_data)

        place_id = self.next_id
        self.next_id += 1

        place = {
            'id': place_id,
            'name': place_data['name'],
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'owner': place_data.get('owner', None),
            'amenities': place_data.get('amenities', [])
        }

        self.places[place_id] = place
        return place

    def get_place(self, place_id):
        if place_id not in self.places:
            raise ValueError(f"Place with ID {place_id} not found")

        return self.places[place_id]
=======
    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass
>>>>>>> d1d0ebd96edd01586f5e2001e6196d4116b38318

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
<<<<<<< HEAD
        if place_id not in self.places:
            raise ValueError(f"Place with ID {place_id} not found")

        if 'price' in place_data:
            self.validate_price(place_data['price'])
        if 'latitude' in place_data or 'longitude' in place_data:
            self.validate_coordinates(place_data.get('latitude', self.places[place_id]['latitude']),
                                     place_data.get('longitude', self.places[place_id]['longitude']))

        self.places[place_id].update(place_data)
        return self.places[place_id]

class ReviewManager:
    def __init__(self):
        self.reviews = {}

    def add_review(self, place_id, data):
        if place_id not in self.reviews:
            self.reviews[place_id] = []

        review_id = len(self.reviews[place_id]) + 1
        review = {
            'id': review_id,
            'data': data
        }
        self.reviews[place_id].append(review)
        return review

    def get_reviews_by_place_id(self, place_id):
        return self.reviews.get(place_id, [])

    def get_review_by_id(self, place_id, review_id):
        if place_id not in self.reviews:
            return None

        for review in self.reviews[place_id]:
            if review['id'] == review_id:
                return review
        return None

    def update_review(self, place_id, review_id, data):
        if place_id not in self.reviews:
            return None

        for review in self.reviews[place_id]:
            if review['id'] == review_id:
                review['data'] = data
                return review
        return None
=======
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
>>>>>>> d1d0ebd96edd01586f5e2001e6196d4116b38318

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass