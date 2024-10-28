from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from flask_restx import Namespace


api = Namespace("users", description="User operations")

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        # Checking email uniqueness
        existing_user = self.get_user_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError("Email already registered")

        # Create the new user and add it to the repo
        new_user = User(**user_data)
        self.user_repo.add(new_user)
        return new_user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        users = self.user_repo.get_all()
        return [user.__dict__ for user in users]

    def get_user_by_email(self, email):
        if not email:
            raise ValueError("Email cannot be empty.")
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        user_to_update = self.get_user(user_id)

        if not user_to_update:
            raise ValueError("User not found")

        # Checking email uniqueness
        existing_user = self.get_user_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError("Email already registered")

        self.user_repo.update(user_id, user_data)
        return user_to_update

    def create_amenity(self, amenity_data):
        # Checking amenity name uniqueness
        existing_amenity = self.amenity_repo.get_by_attribute('name', amenity_data.get('name'))
        if existing_amenity:
            raise ValueError("Amenity already registered")
        new_amenity = Amenity(**amenity_data)

        # Create the new amenity and add it to the repo
        self.amenity_repo.add(new_amenity)

        return new_amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [amenity.__dict__ for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        amenity_to_update = self.get_amenity(amenity_id)

        if not amenity_to_update:
            raise ValueError("error: Amenity not found")

        # Checking name uniqueness
        new_name = amenity_data.get('name')
        existing_amenity = self.amenity_repo.get_by_attribute('name', new_name)
        if existing_amenity:
            raise ValueError("Amenity name already registered")

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity_to_update


    def create_place(self, place_data):
        # Checking Owner existence

        existing_owner = self.user_repo.get_by_attribute('id', place_data.get('owner_id'))
        if not existing_owner:
            raise ValueError("Owner_ID must be valid to allow place creation.")

        # Replacing owner_id by its corresponding User instance
        place_data.pop('owner_id')
        place_data['owner'] = existing_owner

        print(f"replaced place data with user : {place_data}")

        # Create the new place and add it to the repo
        new_place = Place(**place_data)
        self.place_repo.add(new_place)
        return new_place


    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieves all places"""
        places = self.place_repo.get_all()
        
        # Convert each Place instance to a dictionary
        place_dicts = []
        for place in places:
            if hasattr(place, "to_dict"):
                place_dicts.append(place.to_dict())
            else:
                # Manually convert nested User and Amenity objects to dictionaries
                place_dict = place.__dict__.copy()  # Make a copy of place's attributes
                if isinstance(place_dict.get("user"), User):
                    place_dict["user"] = place_dict["user"].to_dict()
                if isinstance(place_dict.get("amenity"), Amenity):
                    place_dict["amenity"] = place_dict["amenity"].to_dict()
                place_dicts.append(place_dict)
        
        return place_dicts

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass
    
    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass


    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass

facade = HBnBFacade()
