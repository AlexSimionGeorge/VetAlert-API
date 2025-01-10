from firebase_admin import firestore
from api.models.Veterinarian import Veterinarian
from api.repository.CollectionsConfig import VeterinarianCollection

veterinarian_collection = firestore.client().collection(VeterinarianCollection)

class VeterinarianRepository:
    @staticmethod
    def veterinarian_exists(uid: str) -> bool:
        """
        Check if the veterinarian already exists in the Firestore database by UID.
        """
        doc_ref = veterinarian_collection.document(uid)
        try:
            return doc_ref.get().exists
        except Exception as e:
            print(f"Error checking if veterinarian exists: {e}")
            return False

    @staticmethod
    def create_veterinarian(uid: str, veterinarian: Veterinarian) -> None:
        """
        Create a new veterinarian in the Firestore database.
        """
        doc_ref = veterinarian_collection.document(uid)
        doc_ref.set(veterinarian.to_dict())
