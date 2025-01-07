from models.card import Card
from app.db_config import Config
from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DBNAME]  # Database name
collection = db[Config.CARD_COLLECTION]  # Collection name

# read the json file cardsraw.json, convert it to a list of Card objects and insert them into the database

with open("cardsraw.json", "r") as file:
    card_data = json.load(file).get('data', [])
    cards = [Card.from_dict(card) for card in card_data]
    collection.insert_many([card.to_dict() for card in cards])

print("Cards inserted into the database.")