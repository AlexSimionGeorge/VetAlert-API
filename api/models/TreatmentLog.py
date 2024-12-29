from typing import Optional

class TreatmentLog:
    def __init__(self, animal: str, item: str, date: int, quantity: str, tlid: Optional[str] = None):
        self.tlid = tlid
        self.animal = animal
        self.item = item
        self.date = date
        self.quantity = quantity

    def to_dict(self):
        return {
            'tlid': self.tlid,
            'animal': self.animal,
            'item': self.item,
            'date': self.date,
            'quantity': self.quantity
        }

    def to_db_format(self):
        return {
            'animal': self.animal,
            'item': self.item,
            'date': self.date,
            'quantity': self.quantity
        }

    @staticmethod
    def from_post_request(data: dict):
        return TreatmentLog(
            animal=data.get('animal'),
            item=data.get('item'),
            date=data.get('date'),
            quantity=data.get('quantity')
        )

    @staticmethod
    def from_dict_db(dictionary: dict, tlid: str):
        return TreatmentLog(
            tlid=tlid,
            animal=dictionary.get('animal'),
            item=dictionary.get('item'),
            date=dictionary.get('date'),
            quantity=dictionary.get('quantity')
        )
