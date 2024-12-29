from firebase_admin import firestore

from api.models.Animal import Animal
from api.repository.CollectionsConfig import AnimalCollection

animal_collection = firestore.client().collection(AnimalCollection)

class AnimalRepository:
    @staticmethod
    def add_animal(animal: Animal):
        doc_ref = animal_collection.document()
        doc_ref.set(animal.to_db_format())
        animal.aid = doc_ref.id
        return animal

    @staticmethod
    def get_animal(animal_id: str):
        doc = animal_collection.document(animal_id).get()
        if doc.exists:
            return Animal.from_dict_db(doc.to_dict(), doc.id)
        return None

    @staticmethod
    def update_animal(animal_id: str, animal: Animal):
        doc_ref = animal_collection.document(animal_id)
        doc_ref.set(animal.to_db_format())

    @staticmethod
    def delete_animal(animal_id: str):
        animal_collection.document(animal_id).delete()

    @staticmethod
    def find_by_veterinarian_id(veterinarian_id: str):
        query = animal_collection.where("veterinarian", "==", veterinarian_id).stream()
        animals = [Animal.from_dict_db(doc.to_dict(), doc.id) for doc in query]
        return animals