#!/usr/bin/python3
'''
This module defines the Business Logic User class
'''
from base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        
        if len(name) > 50:
            raise ValueError("Name must be 50 chars maximum")
        else:
            self.name = name
