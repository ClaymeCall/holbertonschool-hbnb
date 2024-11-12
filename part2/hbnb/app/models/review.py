from app.models.base_model import BaseModel
from app.models.user import User


users_list = []
places_list = []


class Review(BaseModel):
    def __init__(self, place_id, user, rating, text):
        """Initialize Review class with BaseModel"""
        super().__init__()
        self.text = text
        self.place_id = place_id
        self.user = user  # User who wrote review
        self.rating = rating  # Setter use

    @property
    def rating(self):
        """Return rating"""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set the rating, ensuring it is an integer from 1 to 5"""
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer.")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be from 1 to 5.")
        self._rating = value

    @property
    def text(self):
        """Return the text of the review"""
        return self._text

    @text.setter
    def text(self, value):
        """Set the text with a minimum and maximum character length requirement"""
        if not isinstance(value, str):
            raise TypeError("Text must be a string.")
        if len(value) < 4:
            raise ValueError("Text must be at least 4 characters long.")
        if len(value) > 100:
            raise ValueError("Text must be 100 characters maximum.")
        self._text = value

    @property
    def place_id(self):
        """Return the id of the place being reviewed"""
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        """Set the id of the place being reviewed"""
        self._place_id = value

    @property
    def user(self):
        """Return the user who wrote the review"""
        return self._user

    @user.setter
    def user(self, value):
        """Set the user who wrote the review, ensuring it's a User instance"""
        if not isinstance(value, User):
            raise TypeError("User must be an instance of the User class.")
        self._user = value

    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "rating": self.rating,
            "text": self.text,
            "user": self.user.to_dict() if isinstance(self.user, User) else None,
        }
