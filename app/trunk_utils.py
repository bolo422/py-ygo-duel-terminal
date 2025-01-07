from .models.deck import Deck
from .models.trunk import Trunk

def move_card_from_deck_to_trunk(deck: Deck, deck_type: str, trunk: Trunk, card_id: str, quantity: int = 1):
    """Move a card from a deck to a trunk."""
    if deck.remove_card(card_id, quantity, deck_type):
        trunk.add_card(card_id, quantity)
        print(f"Moved {quantity} of card {card_id} from deck to trunk.")
    else:
        print(f"Card {card_id} not found in deck.")

def move_card_from_trunk_to_deck(deck: Deck, deck_type: str, trunk: Trunk, card_id: str, quantity: int = 1):
    """Move a card from a trunk to a deck."""
    if trunk.remove_card(card_id, quantity):
        deck.add_card_by_id(card_id, quantity, deck_type)
        print(f"Moved {quantity} of card {card_id} from trunk to deck.")
    else:
        print(f"Card {card_id} not found in trunk.")

def move_card_deck_to_deck(deck: Deck, deck_type: str, card_id: str, quantity: int = 1):
    """Move a card from one deck to another."""
    if deck.remove_card(card_id, quantity, deck_type):
        deck.add_card_by_id(card_id, quantity, deck_type)
        print(f"Moved {quantity} of card {card_id} from deck to deck.")
    else:
        print(f"Card {card_id} not found in deck.")