from app.models.amenity import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def add(self, amenity):
        db.session.add(amenity)
        db.session.commit()

    def update(self, amenity_id, data):
        amenity = self.get(amenity_id)
        if amenity:
            for key, value in data.items():
                setattr(amenity, key, value)
            db.session.commit()
""""
    def delete(self, amenity_id):

        amenity = self.get(amenity_id)
        
        if amenity:
            db.session.delete(amenity)
            db.session.commit()

    def get(self, amenity_id):
        return self.model.query.get(amenity_id)

    def get_all(self):
        return self.model.query.all()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
"""