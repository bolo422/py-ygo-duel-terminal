from pymongo import MongoClient
from dotenv import load_dotenv
import os

class Config:
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DBNAME = "YGO"
    CARD_COLLECTION = "cards"

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DBNAME]
    cards_collection = db[CARD_COLLECTION]
