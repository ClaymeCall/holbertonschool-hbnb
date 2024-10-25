from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review


class Place(BaseModel):
    def __init__(
        self,
        title,
        description=None,
        price=None,
        latitude=None,
        longitude=None,
        owner_id=None,
        owner=None,
        amenities=None
    ):
        """Initialize the Place class with title, description, location, price and owner"""
        super().__init__()

        self.reviews = []
        self.amenities = amenities if amenities is not None else []

        #valid Title
        if not isinstance(title, str) or len(title) > 1000:
            raise ValueError("Fill with a 100 max length characters string title")
        self.title = title

        #valid description
        if description is None:
            self.description = "Fill with a description"
        else:
            self.description = description

        #Valid price
        if price is not None:
            if not isinstance(price, (int, float)):
                raise ValueError("Price must be a number")
            if price < 0:
                raise ValueError("Price must be a positive number")
        self.price = price

        # Valid Latitude
        if latitude is not None:
            if not isinstance(latitude, (int, float)):
                raise ValueError("Latitude must be a number")
            if not (-90 <= latitude <= 90):
                raise ValueError("Latitude must be between -90.0° and 90.0°")
        self.latitude = latitude

        # Valid Longitude
        if longitude is not None:
            if not isinstance(longitude, (int, float)):
                raise ValueError("Longitude must be a number")
            if not (-180 <= longitude <= 180):
                raise ValueError("Longitude must be between -180.0° and 180.0°")
        self.longitude = longitude

        # Valid owner_id
        if owner_id is not None:
            if not isinstance(owner_id, str):
                raise ValueError("Owner ID must be a valid string")
        self.owner_id = owner_id

        # Valid owner
        if owner is not None:
            if not isinstance(owner, User):
                raise ValueError("Owner must be a valid user of our benger system")
        self.owner = owner


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

    def get_owner_info(self):
        """Return dic of the owner's infos if he is setted"""
        if self.owner:
            return {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email,
                "is_admin": self.owner.is_admin if hasattr(self.owner, "is_admin") else False
            }
        return None

    def get_all_info(self):
        """return all info of place with amenities and review dedicated"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.get_owner_info(),
            "amenities": [amenity.name for amenity in self.amenities],
            "reviews": [review.text for review in self.reviews],
        }
