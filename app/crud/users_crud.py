from models.user import User
from app.db_config import Config
from pymongo import MongoClient

client = Config.users_collection

class UserCRUD:
    def create_user(self, user: User):
        """Create a new user in the database."""
        if not self.get_user_by_username(user.username):
            client.insert_one(user.to_dict())
            print(f"User for {user.username} created.")
        else:
            print(f"User for {user.username} already exists.")

    def get_user_by_username(self, username: str) -> User:
        """Fetch a user from the database by username."""
        user_data = client.find_one({"username": username})
        if user_data:
            return User.from_dict(user_data)
        return None

    def delete_user(self, username: str):
        """Delete a user from the database."""
        result = client.delete_one({"username": username})
        if result.deleted_count > 0:
            print(f"User for {username} deleted.")
        else:
            print(f"User for {username} not found.")