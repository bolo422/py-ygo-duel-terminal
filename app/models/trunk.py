from pymongo import MongoClient
from .deck import Deck
from app.models.card import Card
from app.card_search import search_card_by_id

class Trunk:
    def __init__(self, username, cards=None, deck=None):
        self.username = username
        self.cards = cards if cards else {}
        self.deck = deck if deck else Deck()

    def add_card(self, card_id:int, quantity=1):
        """Add a card to the trunk."""

        card = search_card_by_id(card_id)

        if card in self.cards:
            self.cards[card] += quantity
        else:
            self.cards[card] = quantity

    def remove_card(self, card_id:int, quantity=1):
        """Remove a card from the trunk."""

        card = search_card_by_id(card_id)

        if card in self.cards:
            if self.cards[card] > quantity:
                self.cards[card] -= quantity
            else:
                del self.cards[card]
        else:
            print("Card not found in trunk.")

    def to_dict(self):
        """Convert Trunk object to dictionary."""
        return {
            "username": self.username,
            "cards": {str(card.id): quantity for card, quantity in self.cards.items()},
            "deck": self.deck.to_dict()
        }
    
    def to_detailed_dict(self):
        """Convert Trunk object to a detailed dictionary with card details."""
        detailed_cards = []
        for card, quantity in self.cards.items():
            card_dict = card.to_dict()
            for _ in range(quantity):
                detailed_cards.append(card_dict)

        return {
            "username": self.username,
            "cards": detailed_cards,
            "deck": self.deck.to_detailed_dict()
        }
    
    def get_all_cards_map(self):
        """Get all cards in the trunk and deck."""
        combined_map = self.cards.copy()
        deck_map = self.deck.get_cards_map()

        for card_id, quantity in deck_map.items():
            if card_id in combined_map:
                combined_map[card_id] += quantity
            else:
                combined_map[card_id] = quantity

        return combined_map

    @classmethod
    def from_dict(cls, data):
        """Create a Trunk object from a dictionary."""
        return cls(
            data["username"],
            {search_card_by_id(int(card_id)): quantity for card_id, quantity in data["cards"].items()},
            Deck.from_dict(data["deck"])
        )
