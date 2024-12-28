from pydantic import EmailStr
from typing import Optional
import json

class Veterinarian:
    def __init__(self, name: str, email: EmailStr, cabinet_address: Optional[str] = None, phone_number: Optional[str] = None) -> None:
        self.name = name
        self.email = email
        self.cabinet_address = cabinet_address
        self.phone_number = phone_number

    def to_dict(self):
        """
        Converts the Veterinarian object to a dictionary.
        """
        return {
            "name": self.name,
            "email": self.email,
            "cabinet_address": self.cabinet_address,
            "phone_number": self.phone_number,
        }

    def to_json(self):
        """
        Converts the Veterinarian object to a JSON string.
        """
        return json.dumps(self.to_dict())
