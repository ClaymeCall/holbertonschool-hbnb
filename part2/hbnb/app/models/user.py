from app.models.base_model import BaseModel
import re


class User(BaseModel):
    
    EMAIL_REGEX = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'    

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value.isalpha():
            raise TypeError("First name must be a string of letters.")
        elif len(value) > 50:
            raise ValueError("First name must be 50 characters maximum.")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value.isalpha():
            raise TypeError("Last name must be a string of letters.")
        elif len(value) > 50:
            raise ValueError("Last name must be 50 characters maximum.")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.fullmatch(self.EMAIL_REGEX, value):
            raise ValueError("Invalid email format.")
        self._email = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean (True or False).")
        self._is_admin = value

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
