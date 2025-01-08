from pymongo import MongoClient
from app.crud.mongo_utils import convert_all_dict_key_to_string

class TrunkCRUD:
    def __init__(self, db_uri, db_name, collection_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_trunk_by_username(self, username : str):
        """Fetch a trunk by username."""
        return self.collection.find_one({"username": username})

    def create_trunk(self, username : str):
        """Create a new trunk with empty decks."""
        if self.collection.find_one({"username": username}):
            raise ValueError("A trunk with this username already exists.")
        
        trunk = {
            "username": username,
            "trunk_deck": {},
            "main_deck": {},
            "side_deck": {},
            "extra_deck": {}
        }
        self.collection.insert_one(trunk)

    def delete_trunk(self, username : str):
        """Delete a trunk by username."""
        result = self.collection.delete_one({"username": username})
        if result.deleted_count == 0:
            raise ValueError("Trunk not found.")

    def update_trunk(self, username : str, updated_trunk : dict):
        """Update a trunk's decks or other properties."""
        if not self.collection.find_one({"username": username}):
            raise ValueError("Trunk not found.")
        
        updated_trunk = convert_all_dict_key_to_string(updated_trunk)
        # Ensure only allowed fields are updated
        allowed_fields = {"username", "trunk_deck", "main_deck", "side_deck", "extra_deck"}
        filtered_trunk = {k: v for k, v in updated_trunk.items() if k in allowed_fields}
        
        self.collection.update_one(
            {"username": username},
            {"$set": filtered_trunk}
        )