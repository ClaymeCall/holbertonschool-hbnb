#!/usr/bin/env python3
"""This model defines the Business review class"""
import uuid
from datetime import datetime
from part2.hbnb.app.models.base_model import BaseModel
from part2.hbnb.app.models import place


users_list = []
places_list = []


class Review(BaseModel):
    def __init__(self, place, user, rating, text):
        super().__init__()
        self.id = str(uuid.uuid4())  # Unique Id generated of the review
        self.text = text
        self.rating = rating
        self.place = place  # Place being reviewed
        self.user = user  # User who wrote review
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        self.rating = rating
        place.add_review(self)

    # Rating
    @property
    def rating(self):
        """Return rating"""
        return self.rating

    @rating.setter
    def rating(self, value):
        """Frame the rating"""
        if value > 0 or value > 5:
            raise ValueError("Rating must be from 0 to 5")
        self.rating = value

    # Validation process before authorizing review
    def validate_user(self, user_id):
        """Validating user method to authorize adding review"""
        for user in users_list:
            if user.user_id == user_id:
                return user
        raise ValueError("User {} does not exist".format(user_id))

    def validate_place(self, place_id):
        """Validating place method to authorize adding review"""
        for place in places_list:
            if place.place_id == place_id:
                return place
        raise ValueError("User {} does not exist".format(place_id))

    # Get review
    def print_review(self):
        """Print the review as a readble string"""
        return "Review by {} for {}: {} > Rating: {}".format(
            self.user.name, self.place.name, self.text, self.rating
        )
