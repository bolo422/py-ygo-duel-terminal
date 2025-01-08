class Trunk:
    def __init__(self, username, trunk_deck=None, main_deck=None, side_deck=None, extra_deck=None):
        self.username = username
        self.trunk_deck = trunk_deck if trunk_deck else {}
        self.main_deck = main_deck if main_deck else {}
        self.side_deck = side_deck if side_deck else {}
        self.extra_deck = extra_deck if extra_deck else {}

    def _get_deck(self, deckType):
        deck_map = {
            "trunk": self.trunk_deck,
            "trunk_deck": self.trunk_deck,
            "main": self.main_deck,
            "main_deck": self.main_deck,
            "side": self.side_deck,
            "side_deck": self.side_deck,
            "extra": self.extra_deck,
            "extra_deck": self.extra_deck
        }
        return deck_map.get(deckType)

    def add_card(self, id, quantity, deckType):
        deck = self._get_deck(deckType)
        if deck is not None:
            deck[id] = deck.get(id, 0) + quantity

    def remove_card_from_deck(self, id, quantity, deckType):
        deck = self._get_deck(deckType)
        if deck and id in deck:
            if deck[id] > quantity:
                deck[id] -= quantity
            else:
                del deck[id]

    def get_all_cards(self):
        combined = {}
        for deck in [self.trunk_deck, self.main_deck, self.side_deck, self.extra_deck]:
            for id, quantity in deck.items():
                combined[id] = combined.get(id, 0) + quantity
        return combined

    def get_cards(self, id, deckType):
        deck = self._get_deck(deckType)
        return deck.get(id, 0) if deck else 0

    def move_cards(self, id, quantity, originDeckType, destinationDeckType):
        id = str(id)
        origin_deck = self._get_deck(originDeckType)
        destination_deck = self._get_deck(destinationDeckType)

        if id in origin_deck:
            origin_quantity = origin_deck[id]
            if origin_quantity > quantity:
                origin_deck[id] -= quantity
            else:
                quantity = origin_quantity
                del origin_deck[id]

            destination_deck[id] = destination_deck.get(id, 0) + quantity

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data["username"],
            trunk_deck=data.get("trunk_deck", {}),
            main_deck=data.get("main_deck", {}),
            side_deck=data.get("side_deck", {}),
            extra_deck=data.get("extra_deck", {})
        )

    def to_dict(self):
        return {
            "username": self.username,
            "trunk_deck": self.trunk_deck,
            "main_deck": self.main_deck,
            "side_deck": self.side_deck,
            "extra_deck": self.extra_deck
        }
