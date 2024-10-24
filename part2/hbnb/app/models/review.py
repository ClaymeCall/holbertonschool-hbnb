from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        """Initialize Review class with BaseModel"""
        super().__init__()
        self.text = text
        self.rating = rating  # Setter use
        self.place = place  # Place being reviewed
        self.user = user  # User who wrote review

    # Rating
    @property
    def rating(self):
        """Return rating"""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Frame the rating"""
        if value < 0 or value > 5:
            raise ValueError("Rating must be from 0 to 5")
        self._rating = value

    # Validation process before authorizing review
    def validate_user(self, user_list, user_id):
        """Validating user method to authorize adding review"""
        for user in user_list:
            if user.user_id == user_id:
                return user
        raise ValueError("User {} does not exist".format(user_id))

    def validate_place(self, place_list, place_id):
        """Validating place method to authorize adding review"""
        for place in place_list:
            if place.place_id == place_id:
                return place
        raise ValueError("User {} does not exist".format(place_id))

    # Get a review by ID
    def print_review(self):
        """Print the review as a readble string"""
        return "Review by {} for {}: {} > Rating: {}".format(
            self.user.name, self.place.name, self.text, self.rating
        )
