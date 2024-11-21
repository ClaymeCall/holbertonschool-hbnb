from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True # This prevents SQLAlchemy to create a table for this class

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
