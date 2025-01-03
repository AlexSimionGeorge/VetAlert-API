from google.oauth2.id_token import verify_firebase_token
from pydantic import EmailStr
from typing import Optional, List

class Owner:
    def __init__(self, name: str, email: EmailStr, pets: List[str], veterinarian: str, oid: Optional[str] = None):
        self.oid = oid
        self.name = name
        self.email = email
        self.pets = pets
        self.veterinarian = veterinarian

    def to_dict(self):
        return {
            'oid': self.oid,
            "name": self.name,
            "email": self.email,
            "pets": self.pets,
            "veterinarian": self.veterinarian,
        }

    def to_db_format(self):
        return {
            "name": self.name,
            "email": self.email,
            "pets": self.pets,
            "veterinarian": self.veterinarian,
        }

    @staticmethod
    def from_post_request(data: dict, uid: str):
        return Owner(
            name=data.get("name"),
            email=data.get("email"),
            pets=data.get("pets", []),
            veterinarian=uid
        )

    @staticmethod
    def from_put_request(data: dict):
        return Owner(
            name=data.get("name"),
            email=data.get("email"),
            pets=data.get("pets", []),
            veterinarian=data.get("veterinarian")
        )

    @classmethod
    def from_dict_db(cls, dictionary: dict, oid: str):
        return Owner(
            oid=oid,
            name=dictionary.get("name"),
            email=dictionary.get("email"),
            pets=dictionary.get("pets", []),
            veterinarian=dictionary.get("veterinarian")
        )

    def merge_with(self, old_owner: 'Owner'):
        self.name = self.name or old_owner.name
        self.email = self.email or old_owner.email
        self.veterinarian = self.veterinarian or old_owner.veterinarian
