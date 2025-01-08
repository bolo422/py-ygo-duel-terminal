from app.ygo_pro_integration import YGOProAPI
from app.crud.cards_crud import find_card_by_id, insert_card, find_card_by_name, find_cards_by_ids
from app.models.card import Card

def search_card_by_id(card_id):
    """Search for a card by ID. Fetch from API and save to DB if not found."""
    card = find_card_by_id(int(card_id))
    
    if card:
        print(f"Card found in database: {card['name']}")
        card = Card.from_dict(card)
    else:
        print(f"Card with ID {card_id} not found in database. Fetching from API...")
        card_data = YGOProAPI.search_cards(id=card_id)
        card_data = [Card.from_dict(card) for card in card_data]
        if card_data:
            # Assume fetch_card_info returns a list of cards; take the first one
            print("card_data:", card_data)
            card_to_save = card_data[0]
            insert_card(card_to_save)
            print(f"Card {card_to_save.name} saved to database.")
            card = card_to_save
        else:
            print("No card data found from API.")

    return card

def search_cards_by_ids(card_ids):
    """Search for cards by IDs."""
    cards = find_cards_by_ids(card_ids)
    cards = [Card.from_dict(card) for card in cards]
    return cards

def search_card_by_name(card_name):
    """Search for a card by name."""
    card = find_card_by_name(card_name)
    if card:
        print(f"Card found in database: {card['name']}")
        card = Card.from_dict(card)
    else:
        print(f"Card with name {card_name} not found in database. Fetching from API...")
        card_data = YGOProAPI.search_cards(name=card_name)
        card_data = [Card.from_dict(card) for card in card_data]
        if card_data:
            # Assume fetch_card_info returns a list of cards; take the first one
            card_to_save = card_data[0]
            insert_card(card_to_save)
            print(f"Card {card_to_save.name} saved to database.")
            card = card_to_save
        else:
            print("No card data found from API.")

        return card