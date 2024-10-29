from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner
    ):
        """Initialize the Place class with title, description, location, price and owner"""
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

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

    @price.setter
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

    '''
    def add_review(self, review):
        """Add review to place."""
        if not isinstance(review, Review):
            raise ValueError("Review must a valid")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add amenity to place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be valid")
        self.amenities.append(amenity)
    '''

    def get_owner_info(self):
        """Return dic of the owner's infos if set"""
        if self.owner:
            return {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email,
                "is_admin": self.owner.is_admin
            }
        return None
    
    def to_dict(self):
        """return all info of place with amenities and review dedicated"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict() if isinstance(self.owner, User) else None,
            #"amenities": [amenity.name for amenity in self.amenities],
            #"reviews": [review.text for review in self.reviews],
        }
