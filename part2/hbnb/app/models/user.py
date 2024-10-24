#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5
import re

# This regex is used to verify valid emails.
regex = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'

class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, first_name, last_name, email, is_admin=False, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

        '''Setting email value'''
        if re.fullmatch(regex, email):
            self.email = email
        else:
            raise ValueError("Invalid email format.")

        '''Setting first name value'''
        if not first_name.isalpha():
            raise TypeError("First name must be a string of letters.")
        elif len(first_name) > 50:
            raise ValueError("First name must be 50 chars maximum")
        else:
            self.first_name = first_name

        '''Setting last name value'''
        if not last_name.isalpha():
            raise TypeError("Last name must be a string of letters.")
        elif len(last_name) > 50:
            raise ValueError("Last name must be 50 chars maximum")
        else:
            self.last_name = last_name

        '''Setting admin boolean value'''
        if type(is_admin) is not bool:
            raise TypeError("is_admin must be True or False.")
        else:
            self.is_admin = is_admin

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

