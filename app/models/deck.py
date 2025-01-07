from .card import Card
from app.card_search import search_card_by_id

class Deck:
    def __init__(self, main_deck=None, side_deck=None, extra_deck=None):
        self.main_deck = main_deck if main_deck else {}
        self.side_deck = side_deck if side_deck else {}
        self.extra_deck = extra_deck if extra_deck else {}

    def add_card(self, card, quantity, deck_type):
        """Add a card to the deck."""
        if deck_type == "main":
            self.main_deck.extend([card] * quantity)
        elif deck_type == "side":
            self.side_deck.extend([card] * quantity)
        elif deck_type == "extra":
            self.extra_deck.extend([card] * quantity)
        else:
            print("Invalid deck type.")

    def add_card_by_id(self, card_id, quantity, deck_type):
        """Add a card to the deck by its ID."""
        card = search_card_by_id(card_id)
        if card:
            self.add_card(card, quantity, deck_type)
        else:
            print("Card not found.")

    def remove_card(self, card, quantity, deck_type):
        """Remove a card from the deck."""
        # decks are maps of Card:int
        # if quantity is equal to or greater than the number of cards in the deck, remove the card from the deck
        # if is lesser, decrement the quantity of the card in the deck
        if deck_type == "main":
            deck = self.main_deck
        elif deck_type == "side":
            deck = self.side_deck
        elif deck_type == "extra":
            deck = self.extra_deck
        else:
            print("Invalid deck type.")
            return
        
        if card in deck:
            if deck[card] > quantity:
                deck[card] -= quantity
            else:
                del deck[card]

    def remove_card_by_id(self, card_id, quantity, deck_type):
        """Remove a card from the deck by its ID."""
        # don't search for the card here, its too expensive, just look for the card ID in the deck
        if deck_type == "main":
            deck = self.main_deck
        elif deck_type == "side":
            deck = self.side_deck
        elif deck_type == "extra":
            deck = self.extra_deck
        else:
            print("Invalid deck type.")
            return
        
        for card in deck:
            if card.id == card_id:
                if deck[card] > quantity:
                    deck[card] -= quantity
                else:
                    del deck[card]
                return

    def get_cards_map(self):
        """Get a map of card IDs to quantities in the deck."""
        cards_map = {}
        for card in self.main_deck + self.side_deck + self.extra_deck:
            if card in cards_map:
                cards_map[card] += 1
            else:
                cards_map[card] = 1
        return cards_map
    
    def get_cards_map(self, deck_type):
        """Get a map of card IDs to quantities in the deck."""
        cards_map = {}
        if deck_type == "main":
            deck = self.main_deck
        elif deck_type == "side":
            deck = self.side_deck
        elif deck_type == "extra":
            deck = self.extra_deck
        else:
            print("Invalid deck type.")
            return cards_map

        for card in deck:
            if card in cards_map:
                cards_map[card] += 1
            else:
                cards_map[card] = 1
        return cards_map


    def to_dict(self):
        """Convert Deck object to dictionary."""
        return {
            "main_deck": {str(card.id): quantity for card, quantity in self.get_cards_map("main").items()},
            "side_deck": {str(card.id): quantity for card, quantity in self.get_cards_map("side").items()},
            "extra_deck": {str(card.id): quantity for card, quantity in self.get_cards_map("extra").items()}
        }
    
    def detail_cards(self, cards):
        detailed_cards = []
        for card, quantity in cards.items():
            card_dict = card.to_dict()
            for _ in range(quantity):
                detailed_cards.append(card_dict)
        return detailed_cards
    
    def to_detailed_dict(self):
        """Convert Deck object to a detailed dictionary with card details."""
        return {
            "main_deck": self.detail_cards(self.get_cards_map("main")),
            "side_deck": self.detail_cards(self.get_cards_map("side")),
            "extra_deck": self.detail_cards(self.get_cards_map("extra"))
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Deck object from a dictionary."""
        return cls(
            # in the dictionary, cards are stored as card IDs to quantities, so we need to convert them to Card objects
            [search_card_by_id(int(card_id)) for card_id, quantity in data["main_deck"].items() for _ in range(quantity)],
            [search_card_by_id(int(card_id)) for card_id, quantity in data["side_deck"].items() for _ in range(quantity)],
            [search_card_by_id(int(card_id)) for card_id, quantity in data["extra_deck"].items() for _ in range(quantity)]
        )
