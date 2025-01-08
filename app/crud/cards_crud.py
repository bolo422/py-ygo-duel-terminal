from app.db_config import Config

cards_collection = Config.cards_collection

def find_card_by_id(card_id):
    """Search for a card in the database by its ID."""
    # convert id to number
    return cards_collection.find_one({"id": int(card_id)})

def find_cards_by_ids(card_ids):
    """Search for cards in the database by their IDs."""
    return cards_collection.find({"id": {"$in": [int(card_id) for card_id in card_ids]}})

def find_card_by_name(card_name):
    """Search for a card in the database by its name, case-insensitive."""
    return cards_collection.find_one({"name": {"$regex": card_name, "$options": "i"}})

def find_card_by_type(card_type):
    """Search for a card in the database by its type, case-insensitive."""
    return cards_collection.find_one({"type": {"$regex": card_type, "$options": "i"}})

def find_card_by_humanReadableCardType(humanReadableCardType):
    """Search for a card in the database by its humanReadableCardType, case-insensitive."""
    return cards_collection.find_one({"humanReadableCardType": {"$regex": humanReadableCardType, "$options": "i"}})

def find_cards_by_typeline(typeline):
    return cards_collection.find({"typeline": {"$all": typeline}})

def find_cards_by_atk(min_atk, max_atk):
    """Search for a card in the database by its attack points."""
    return cards_collection.find({"atk": {"$gte": min_atk, "$lte": max_atk}})

def find_cards_by_def(min_def, max_def):
    """Search for a card in the database by its defense points."""
    return cards_collection.find({"def": {"$gte": min_def, "$lte": max_def}})

def find_cards_by_atk_def(min_atk, max_atk, min_def, max_def):
    """Search for a card in the database by its attack and defense points."""
    return cards_collection.find({
        "atk": {"$gte": min_atk, "$lte": max_atk},
        "def": {"$gte": min_def, "$lte": max_def}
    })

def find_cards_by_level(level):
    """Search for a card in the database by its level."""
    return cards_collection.find({"level": level})

def find_cards_by_attribute(attribute):
    """Search for a card in the database by its attribute."""
    return cards_collection.find({"attribute": attribute})

def insert_card(card):
    """Insert a card into the database."""
    if not find_card_by_id(card.id):
        cards_collection.insert_one(card.to_dict())

def insert_cards(cards):
    """Insert many cards into the database."""
    cards_collection.insert_many([card.to_dict() for card in cards])