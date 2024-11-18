'''
This module defines the Business Logic Amenity class.
'''
import uuid
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel
from app import db


class Amenity(BaseModel):

    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters maximum.")
        elif len(value) < 1:
            raise ValueError("Name must have at least 1 character.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
