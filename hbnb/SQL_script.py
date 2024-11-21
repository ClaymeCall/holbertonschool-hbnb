import os
from datetime import timedelta
from app import create_app, db
from app.services import facade
from flask_jwt_extended import create_access_token

app = create_app()

with app.app_context():
    # Delete the existing database file if it exists
    db_path = os.path.join(app.instance_path, 'development.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing development.db deleted.")
    
    # Recreate the database
    db.create_all()
    print("New database created.")

    # Create users and generate tokens
    user_data_list = [
        {"first_name": "Nicolas", "last_name": "Martinez", "email": "n.martinez@uwu.com", "password": "string", "is_admin": False},
        {"first_name": "Clément", "last_name": "Callejon", "email": "c.callejon@uwu.com", "password": "string", "is_admin": False},
        {"first_name": "David", "last_name": "Vaucheret", "email": "d.vaucheret@uwu.com", "password": "string", "is_admin": False},
        {"first_name": "Louis", "last_name": "Genty", "email": "l.genty@uwu.com", "password": "string", "is_admin": False}
    ]

    users = []
    tokens = {}

    for user_data in user_data_list:
        # Create user
        user = facade.create_user(user_data)
        users.append(user)
        print(f"User {user.first_name} {user.last_name} created.")

        # Generate JWT token
        token = create_access_token(
            identity={"id": str(user.id), "is_admin": user.is_admin},
            expires_delta=timedelta(days=2)
        )
        tokens[user.id] = token
        print(f"Token for {user.first_name}: {token}")

    # Nicolas creates a place "Cosy Appartment"
    nicolas = users[0]
    cosy_apt_data = {
        "title": "Cosy Appartment",
        "description": "Come discover the city in this ideally situated apartment.",
        "price": 250.00,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": nicolas.id
    }
    cosy_apt = facade.create_place(cosy_apt_data)
    print(f"Place '{cosy_apt.title}' created by {nicolas.first_name}.")

    # Louis creates a place "Beautiful Chalet"
    louis = users[3]
    btfl_chalet_data = {
        "title": "Beautiful Chalet",
        "description": "Nice and cosy cocoon for discovering the forest life with your family.",
        "price": 300.00,
        "latitude": 45.764,
        "longitude": 4.8357,
        "owner_id": louis.id
    }
    btfl_chalet = facade.create_place(btfl_chalet_data)
    print(f"Place '{btfl_chalet.title}' created by {louis.first_name}.")

    # Create amenities
    amenities_data = [
        {"name": "Wi-Fi"},
        {"name": "Dishwasher"},
        {"name": "A/C"},
        {"name": "Sofa"},
        {"name": "Latte Machine"}
    ]
    amenities = []

    for amenity_data in amenities_data:
        amenity = facade.create_amenity(amenity_data)
        amenities.append(amenity)
        print(f"Amenity '{amenity.name}' created.")

    # Associate amenities to places
    facade.add_amenity_to_place(cosy_apt.id, amenities[0].name)
    facade.add_amenity_to_place(cosy_apt.id, amenities[2].name)

    facade.add_amenity_to_place(btfl_chalet.id, amenities[1].name)
    facade.add_amenity_to_place(btfl_chalet.id, amenities[3].name)
    facade.add_amenity_to_place(btfl_chalet.id, amenities[4].name)
    print(f"Amenities associated to places.")

    # Clément and David create reviews for "Cosy Appartment"
    review_data_list = [
        {"place_id": cosy_apt.id, "rating": 5, "text": "This flat was amazing and all the commodities were there. I recommend !", "user_id": users[1].id},  # Clément
        {"place_id": cosy_apt.id, "rating": 2, "text": "I would have liked a bit more light in the living room.", "user_id": users[2].id}  # David
    ]

    for review_data in review_data_list:
        review = facade.create_review(review_data)
        print(f"Review created: '{review.text}' by user ID {review.user_id}.")

    # Nicolas creates a review for "Beautiful Chalet"
    nicolas_review_chalet_data = {
        "place_id": btfl_chalet.id,
        "rating": 4,
        "text": "A bit cold, but perfect other than that !",
        "user_id": nicolas.id
    }
    nicolas_review_chalet = facade.create_review(nicolas_review_chalet_data)
    print(f"Review created: '{nicolas_review_chalet.text}' by {nicolas.first_name}.")
