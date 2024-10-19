'''
This module defines the Business Logic User class.
'''
from base_model import BaseModel
import re

# This regex is used to verify valid emails.
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

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
            raise TypeError("First name must be a string of letters.")
        elif len(last_name) > 50:
            raise ValueError("Last name must be 50 chars maximum")
        else:
            self.last_name = last_name

        '''Setting admin boolean value'''
        if type(is_admin) is not bool:
            raise TypeError("is_admin must be True or False.")
        else:
            self.is_admin = is_admin
