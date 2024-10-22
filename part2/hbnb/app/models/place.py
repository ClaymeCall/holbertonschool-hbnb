from base_model import BaseModel
from user import User
from review import Review


class Place(BaseModel):
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
