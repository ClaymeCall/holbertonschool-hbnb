import token
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review


class Place(BaseModel):
    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner,
        token
    ):
        """Initialize the Place class with its specific attributes."""
        super().__init__()

        self.title = title
        self.description = description
        self.token = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.token = token
        self.__amenities = []
        self.__reviews = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        if not (1 <= len(value) <= 100):
            raise ValueError("Title must be between 1 and 100 characters.")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string.")
        if len(value) > 1000:
            raise ValueError("Description must be 1000 characters maximum.")
        self._description = value

    @property
    def price(self):
        return self._price

    @token.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number.")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number.")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be an instance of the User class.")
        self._owner = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        if not isinstance(value, str):
            raise TypeError("Token must be a string.")
        if not value:
            raise ValueError("Token can't be empty.")
        self._token = value


    def add_review(self, review):
        """Add review to place."""
        if not isinstance(review, Review):
            raise ValueError("review must be an instance of the Review class.")
        self.__reviews.append(review)

    def add_amenity(self, amenity):
        """Add amenity to place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an instance of the Amenity class.")

        if amenity in self.__amenities:
            raise ValueError("amenity already registered for that place")
        self.__amenities.append(amenity)

    def to_dict(self):
        """return all info of place with amenities and review dedicated"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.token,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict() if isinstance(self.owner, User) else None,
            "amenities": [amenity.name for amenity in self.__amenities],
            "reviews": [review.text for review in self.__reviews],
            "token": self.token
        }
