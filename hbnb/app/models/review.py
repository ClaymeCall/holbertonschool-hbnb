from app.models.base_model import BaseModel
from app.models.user import User
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "rating": self.rating,
            "text": self.text,
            "user_id": self.user_id,
        }
