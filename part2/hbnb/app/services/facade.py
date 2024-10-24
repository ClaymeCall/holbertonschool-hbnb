from app.persistence.repository import InMemoryRepository

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
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
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

    def validate_price(self, price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")

    def validate_coordinates(self, latitude, longitude):
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Latitude must be between -90 and 90, and longitude must be between -180 and 180.")

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

    def get_all_places(self):
        return list(self.places.values())

    def update_place(self, place_id, place_data):
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

