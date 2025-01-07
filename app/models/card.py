class Card:
    def __init__(self, id, name, typeline, card_type, human_readable_type, frame_type, desc, race, atk, def_, level, attribute, ygoprodeck_url):
        self.id = id
        self.name = name
        self.typeline = typeline
        self.card_type = card_type
        self.human_readable_type = human_readable_type
        self.frame_type = frame_type
        self.desc = desc
        self.race = race
        self.atk = atk
        self.def_ = def_
        self.level = level
        self.attribute = attribute
        self.ygoprodeck_url = ygoprodeck_url
        self.imageUrl = self.build_image_url()  # Generate the image URL

    def build_image_url(self):
        """Generate the image URL using the card's id."""
        base_url = "https://raw.githubusercontent.com/bolo422/YuGiOh-Database/refs/heads/main/Card%20Images/"
        return f"{base_url}{self.id}.png"

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data.get("typeline", None),
            data.get("type"),
            data.get("humanReadableCardType"),
            data.get("frameType", None),
            data.get("desc", ""),
            data.get("race", None),
            data.get("atk", None),
            data.get("def", None),
            data.get("level", None),
            data.get("attribute", None),
            data.get("ygoprodeck_url", None)
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "typeline": self.typeline,
            "type": self.card_type,
            "humanReadableCardType": self.human_readable_type,
            "frameType": self.frame_type,
            "desc": self.desc,
            "race": self.race,
            "atk": self.atk,
            "def": self.def_,
            "level": self.level,
            "attribute": self.attribute,
            "ygoprodeck_url": self.ygoprodeck_url,
            "imageUrl": self.imageUrl
        }
