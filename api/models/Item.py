from typing import Optional

class Item:
    def __init__(self, name: str, code_number: str, expiration_date: int, notes: Optional[str] = None):
        self.name = name
        self.code_number = code_number
        self.expiration_date = expiration_date
        self.notes = notes
