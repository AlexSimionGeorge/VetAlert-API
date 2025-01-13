from datetime import datetime, timezone
from typing import Optional

class Item:
    def __init__(self, name: str, code_number: str, expiration_date: int, veterinarian: str, notes: Optional[str] = None, iid: Optional[str] = None):
        self.iid = iid
        self.name = name
        self.code_number = code_number
        self.expiration_date = expiration_date
        self.notes = notes
        self.veterinarian = veterinarian


    def to_dict(self):
        return {
            'iid': self.iid,
            'name': self.name,
            'code_number': self.code_number,
            # Convert Unix timestamp to ISO 8601 string
            'expiration_date': datetime.fromtimestamp((int(self.expiration_date)), tz=timezone.utc).isoformat(),
            'notes': self.notes,
            'veterinarian': self.veterinarian,
        }


    def to_db_format(self):
        return {
            'name': self.name,
            'code_number': self.code_number,
            'expiration_date': self.expiration_date,
            'notes': self.notes,
            'veterinarian': self.veterinarian,
        }

    @staticmethod
    def from_post_request(data: dict, uid: str):
        return Item(
            name=data.get("name"),
            code_number=data.get("code_number"),
            expiration_date=int(data.get("expiration_date")),
            notes=data.get("notes", ""),
            veterinarian=uid,
        )

    @staticmethod
    def from_put_request(data: dict):
        return Item(
            name=data.get("name"),
            code_number=data.get("code_number"),
            expiration_date=data.get("expiration_date"),
            notes=data.get("notes", ""),
            veterinarian=data.get("veterinarian"),
        )

    @classmethod
    def from_dict_db(cls, dictionary: dict, iid: str):
        return Item(
            iid=iid,
            name=dictionary.get("name"),
            code_number=dictionary.get("code_number"),
            expiration_date=dictionary.get("expiration_date"),
            notes=dictionary.get("notes"),
            veterinarian=dictionary.get("veterinarian"),
        )


    def merge_with(self, old_item: 'Item'):
        self.name = self.name or old_item.name
        self.code_number = self.code_number or old_item.code_number
        self.expiration_date = self.expiration_date or old_item.expiration_date
        self.notes = self.notes or old_item.notes
        self.veterinarian = self.veterinarian or old_item.veterinarian
