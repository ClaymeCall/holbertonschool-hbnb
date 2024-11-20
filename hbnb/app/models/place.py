from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel
from app.models.association_tables import place_amenity
from app import db


class Place(BaseModel):
    """Initialize the Place class with its specific attributes."""
    __tablename__ = 'places'

    title = db.Column(db.String(36), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        backref=db.backref('niquetonpere', lazy=True),
        lazy=True
    )


    @validates("title", include_backrefs=False)
    def title_validation(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        if not (1 <= len(value) <= 100):
            raise ValueError("Title must be between 1 and 100 characters.")
        return value

    @validates("description", include_backrefs=False)
    def description_validation(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string.")
        if len(value) > 1000:
            raise ValueError("Description must be 1000 characters maximum.")
        return value


    @validates("price", include_backrefs=False)
    def price_validation(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        if value < 0:
            raise ValueError("Price cannot be negative.")
        return value


    @validates("latitude", include_backrefs=False)
    def latitude_validation(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number.")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        return value


    @validates("longitude", include_backrefs=False)
    def longitude_validation(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number.")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        return value


    '''
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be an instance of the User class.")
        self._owner = value

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
    '''

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            #"amenities": [amenity.name for amenity in self.amenities],
            #"reviews": [review.text for review in self.reviews],
        }
