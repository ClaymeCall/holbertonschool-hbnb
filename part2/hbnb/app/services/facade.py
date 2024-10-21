from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

class PlaceManager:
    def __init__(self):
        self.places = {}

    def validate_price(self, price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")

    def validate_coordinates(self, latitude, longitude):
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Latitude must be between -90 and 90, and longitude must be between -180 and 180.")

    def create_place(self, place_data):
        # Validate input data
        if 'name' not in place_data or 'price' not in place_data or 'latitude' not in place_data or 'longitude' not in place_data:
            raise ValueError("Missing required fields in place_data.")

        self.validate_price(place_data['price'])
        self.validate_coordinates(place_data['latitude'], place_data['longitude'])

        # Generate a unique ID for the place
        place_id = len(self.places) + 1

        # Create the place
        place = {
            'id': place_id,
            'name': place_data['name'],
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'owner': place_data.get('owner', None),
            'amenities': place_data.get('amenities', [])
        }

        self.places[place_id] = place
        return place

    def get_place(self, place_id):
        if place_id not in self.places:
            raise ValueError("Place with the given ID does not exist.")

        place = self.places[place_id]
        return place

    def get_all_places(self):
        return list(self.places.values())

    def update_place(self, place_id, place_data):
        if place_id not in self.places:
            raise ValueError("Place with the given ID does not exist.")

        # Validate input data
        if 'price' in place_data:
            self.validate_price(place_data['price'])
        if 'latitude' in place_data or 'longitude' in place_data:
            self.validate_coordinates(place_data.get('latitude', self.places[place_id]['latitude']),
                                     place_data.get('longitude', self.places[place_id]['longitude']))

        # Update the place
        place = self.places[place_id]
        place.update(place_data)
        return place

    def __init__(self):
        # Initialiser un dictionnaire pour stocker les avis par place_id
        self.reviews = {}

    def create_review(self, place_id, data):
        """
        Crée un nouvel avis pour une place donnée.

        :param place_id: Identifiant de la place
        :param data: Données de l'avis
        """
        if place_id not in self.reviews:
            self.reviews[place_id] = []

        review_id = len(self.reviews[place_id]) + 1
        review = {
            'id': review_id,
            'data': data
        }
        self.reviews[place_id].append(review)
        return review

    def get_reviews_by_place_id(self, place_id):
        """
        Récupère tous les avis pour une place donnée.

        :param place_id: Identifiant de la place
        :return: Liste des avis
        """
        if place_id not in self.reviews:
            return []
        return self.reviews[place_id]

    def get_review_by_id(self, place_id, review_id):
        """
        Récupère un avis spécifique par son identifiant.

        :param place_id: Identifiant de la place
        :param review_id: Identifiant de l'avis
        :return: Avis spécifique ou None si non trouvé
        """
        if place_id not in self.reviews:
            return None

        for review in self.reviews[place_id]:
            if review['id'] == review_id:
                return review
        return None

    def update_review(self, place_id, review_id, data):
        """
        Met à jour un avis spécifique.

        :param place_id: Identifiant de la place
        :param review_id: Identifiant de l'avis
        :param data: Nouvelles données de l'avis
        :return: Avis mis à jour ou None si non trouvé
        """
        if place_id not in self.reviews:
            return None

        for review in self.reviews[place_id]:
            if review['id'] == review_id:
                review['data'] = data
                return review
        return None
