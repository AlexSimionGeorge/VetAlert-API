from typing import Optional
from api.repository.OwnerRepository import OwnerRepository


class Animal:
    def __init__(self, name: str, species: str, picture: str, owner: str, veterinarian: str, aid:Optional[str] = None):
        self.aid = aid
        self.name = name
        self.species = species
        self.picture = picture
        self.owner = owner
        self.veterinarian = veterinarian

    def to_response(self):
        return {
            'aid': self.aid,
            "name": self.name,
            "species": self.species,
            "picture": self.picture,
            "owner":  OwnerRepository.get_owner(self.owner).to_dict(),
            "veterinarian": self.veterinarian
        }

    def to_dict(self):
        return {
            'aid': self.aid,
            "name": self.name,
            "species": self.species,
            "picture": self.picture,
            "owner": self.owner,
            "veterinarian": self.veterinarian
        }

    def to_db_format(self):
        return {
            "name": self.name,
            "species": self.species,
            "picture": self.picture,
            "owner": self.owner,
            "veterinarian": self.veterinarian
        }

    @staticmethod
    def from_post_request(data: dict, uid: str, picture_url: str):
        return Animal(
            name=data.get("name"),
            species=data.get("species"),
            picture=picture_url,
            owner=data.get("owner"),
            veterinarian=uid
        )

    @staticmethod
    def from_put_request(data: dict, picture_url:str):
        return Animal(
            name=data.get("name"),
            species=data.get("species"),
            picture=picture_url,
            owner=data.get("owner"),
            veterinarian=data.get("veterinarian")
        )

    def merge_with(self, old_animal: 'Animal'):
        """
        Update this animal's attributes with the values from another animal if they are null or missing.
        """
        self.name = self.name or old_animal.name
        self.species = self.species or old_animal.species
        self.picture = self.picture or old_animal.picture
        self.owner =  self.owner if self.owner and self.owner is not None else  old_animal.owner
        self.veterinarian = self.veterinarian or old_animal.veterinarian

    @classmethod
    def from_dict_db(cls, dictionary: dict, aid:str):
        return Animal(
            aid = aid,
            name = dictionary.get("name"),
            species = dictionary.get("species"),
            picture = dictionary.get("picture"),
            owner = dictionary.get("owner"),
            veterinarian = dictionary.get("veterinarian")
        )