from pymongo import MongoClient
from app.models.trunk import Trunk
from app.db_config import Config

class TrunkCRUD:
    def __init__(self):
        self.collection = Config.trunk_collection

    def create_trunk(self, trunk: Trunk):
        """Create a new trunk in the database."""
        if not self.get_trunk_by_username(trunk.username):
            self.collection.insert_one(trunk.to_dict())
            print(f"Trunk for {trunk.username} created.")
            return True, f"Trunk for {trunk.username} created."
        else:
            print(f"Trunk for {trunk.username} already exists.")
            return False, f"Trunk for {trunk.username} already exists."

    def get_trunk_by_username(self, username: str) -> Trunk:
        """Fetch a trunk from the database by username."""
        trunk_data = self.collection.find_one({"username": username})
        if trunk_data:
            return Trunk.from_dict(trunk_data)
        return None

    def delete_trunk(self, username: str):
        """Delete a trunk from the database."""
        result = self.collection.delete_one({"username": username})
        if result.deleted_count > 0:
            print(f"Trunk for {username} deleted.")
        else:
            print(f"Trunk for {username} not found.")

    def update_trunk(self, username: str, trunk: Trunk):
        """Update a trunk in the database."""
        if self.get_trunk_by_username(username):
            self.collection.update_one({"username": username}, {"$set": trunk.to_dict()})
            print(f"Trunk for {username} updated.")
        else:
            print(f"Trunk for {username} not found.")

    def add_card_to_trunk(self, username: str, card_id: int, quantity: int = 1):
        """Add a card to a trunk."""
        trunk = self.get_trunk_by_username(username)
        if trunk:
            trunk.add_card(card_id, quantity)
            self.collection.update_one({"username": username}, {"$set": trunk.to_dict()})
            print(f"Added {quantity} of card {card_id} to {username}'s trunk.")
        else:
            print(f"Trunk for {username} not found.")

    def remove_card_from_trunk(self, username: str, card_id: int, quantity: int = 1):
        """Remove a card from a trunk."""
        trunk = self.get_trunk_by_username(username)
        if trunk:
            trunk.remove_card(card_id, quantity)
            self.collection.update_one({"username": username}, {"$set": trunk.to_dict()})
            print(f"Removed {quantity} of card {card_id} from {username}'s trunk.")
        else:
            print(f"Trunk for {username} not found.")