class User:
    def __init__(self, username, password, privelage):
        self.username = username
        self.password = password
        self.privelage = privelage

    def to_dict(self):
        """Convert User object to dictionary."""
        return {
            "username": self.username,
            "password": self.password,
            "privelage": self.privelage
        }

    @classmethod
    def from_dict(cls, data):
        """Create a User object from a dictionary."""
        return cls(
            data["username"],
            data["password"],
            data["privelage"]
        )