from sqlalchemy.orm import validates
from app.models.base_model import BaseModel
from app import db, bcrypt
import re


class User(BaseModel):
    
    EMAIL_REGEX = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'    

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates("email", include_backrefs=False)
    def validate_email(self, key, value):
        if not re.fullmatch(self.EMAIL_REGEX, value):
            raise ValueError("Invalid email format.")
        return value

    def hash_password(self, value):
        """Hashes the password before storing it."""
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
