from base_model import BaseModel
from user import User
from review import Review

class Place(BaseModel):
    places = {}  # Class attribute to store all places
    reviews = {}  # Class attribute to store all reviews

    def __init__(
        self,
        title=None,
        name=None,
        description=None,
        price=None,
        latitude=None,
        longitude=None,
        owner=None,
    ):
        """Initialize the Place class with both places and reviews dic"""
        super().__init__()
        self.title = title
        self.name = name
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @classmethod
    def create_place(cls, place_data):
        # Validate input data
        if 'title' not in place_data or 'price' not in place_data or 'latitude' not in place_data or 'longitude' not in place_data:
            raise ValueError("Missing required fields in place_data.")

        # Generate a unique ID for the place
        place_id = len(cls.places) + 1

        # Create the place
        place = {
            'id': place_id,
            'title': place_data['title'],
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'owner': place_data.get('owner', None),
            'amenities': place_data.get('amenities', [])
        }

        cls.places[place_id] = place
        return place

    @classmethod
    def get_place(cls, place_id):
        if place_id not in cls.places:
            raise ValueError("Place with the given ID does not exist.")

        place = cls.places[place_id]
        return place

    @classmethod
    def get_all_places(cls):
        return list(cls.places.values())

    @classmethod
    def update_place(cls, place_id, place_data):
        if place_id not in cls.places:
            raise ValueError("Place with the given ID does not exist.")

        # Validate input data
        if 'price' in place_data:
            cls.validate_price(place_data['price'])
        if 'latitude' in place_data or 'longitude' in place_data:
            cls.validate_coordinates(place_data.get('latitude', cls.places[place_id]['latitude']),
                                     place_data.get('longitude', cls.places[place_id]['longitude']))

        # Update the place
        place = cls.places[place_id]
        place.update(place_data)
        return place

    @classmethod
    def add_review_to_place(cls, place_id, data):
        """
        Create a new review for a given place.

        :param place_id: Place ID
        :param data: Review data
        """
        if place_id not in cls.places:
            raise ValueError("Place with the given ID does not exist.")

        if place_id not in cls.reviews:
            cls.reviews[place_id] = []

        review_id = len(cls.reviews[place_id]) + 1
        review = {
            'id': review_id,
            'data': data
        }
        cls.reviews[place_id].append(review)
        return review

    @classmethod
    def get_reviews_by_place_id(cls, place_id):
        """
        Retrieve all reviews for a given place.

        :param place_id: Place ID
        :return: List of reviews
        """
        if place_id not in cls.reviews:
            return []
        return cls.reviews[place_id]

    @classmethod
    def get_review_by_id(cls, place_id, review_id):
        """
        Retrieve a specific review by its ID.

        :param place_id: Place ID
        :param review_id: Review ID
        :return: Specific review or None if not found
        """
        if place_id not in cls.reviews:
            return None

        for review in cls.reviews[place_id]:
            if review['id'] == review_id:
                return review
        return None

    @classmethod
    def update_review(cls, place_id, review_id, data):
        """
        Update a specific review.

        :param place_id: Place ID
        :param review_id: Review ID
        :param data: New review data
        :return: Updated review or None if not found
        """
        if place_id not in cls.reviews:
            return None

        for review in cls.reviews[place_id]:
            if review['id'] == review_id:
                review['data'] = data
                return review
        return None

    @staticmethod
    def validate_price(price):
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")

    @staticmethod
    def validate_coordinates(latitude, longitude):
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Invalid latitude or longitude.")

