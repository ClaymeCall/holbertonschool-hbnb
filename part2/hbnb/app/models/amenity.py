'''
This module defines the Business Logic Amenity class.
'''
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name 

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters maximum.")
        elif len(value) < 1:
            raise ValueError("Name must have at least 1 character.")
        self._name = value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
