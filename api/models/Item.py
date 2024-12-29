from typing import Optional

class Item:
    def __init__(self, name: str, code_number: str, expiration_date: int, veterinarian: str, code: str, notes: Optional[str] = None, iid: Optional[str] = None):
        self.iid = iid
        self.name = name
        self.code_number = code_number
        self.expiration_date = expiration_date
        self.notes = notes
        self.veterinarian = veterinarian
        self.code = code

    def to_dict(self):
        return {
            'iid': self.iid,
            'name': self.name,
            'code_number': self.code_number,
            'expiration_date': self.expiration_date,
            'notes': self.notes,
            'veterinarian': self.veterinarian,
            'code': self.code,
        }

    def to_db_format(self):
        return {
            'name': self.name,
            'code_number': self.code_number,
            'expiration_date': self.expiration_date,
            'notes': self.notes,
            'veterinarian': self.veterinarian,
            'code': self.code,
        }

    @staticmethod
    def from_post_request(data: dict, uid: str):
        return Item(
            name=data.get("name"),
            code_number=data.get("code_number"),
            expiration_date=data.get("expiration_date"),
            notes=data.get("notes", ""),
            veterinarian=uid,
            code=data.get("code"),
        )

    @staticmethod
    def from_put_request(data: dict):
        return Item(
            name=data.get("name"),
            code_number=data.get("code_number"),
            expiration_date=data.get("expiration_date"),
            notes=data.get("notes", ""),
            veterinarian=data.get("veterinarian"),
            code=data.get("code"),
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
            code=dictionary.get("code"),
        )
