from pydantic import EmailStr

class Owner:
    def __init__(self, name: str, email: EmailStr, pets: list[str]):
        self.name = name
        self.email = email
        self.pets = pets

