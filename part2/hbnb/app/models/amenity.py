'''
This module defines the Business Logic Amenity class.
'''
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if len(name) > 50:
            raise ValueError("Name must be 50 characters maximum.")
        elif len(name) < 1:
            raise ValueError("Name must have at least 1 character.")
        
        self.name = name
