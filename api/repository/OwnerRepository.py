from firebase_admin import firestore

from api.models.Owner import Owner
from api.repository.CollectionsConfig import OwnerCollection

owner_collection = firestore.client().collection(OwnerCollection)

class OwnerRepository:
    @staticmethod
    def add_owner(owner: Owner):
        doc_ref = owner_collection.document()
        doc_ref.set(owner.to_db_format())
        owner.oid = doc_ref.id
        return owner

    @staticmethod
    def get_owner(owner_id: str):
        doc = owner_collection.document(owner_id).get()
        if doc.exists:
            return Owner.from_dict_db(doc.to_dict(), doc.id)
        return None

    @staticmethod
    def update_owner(owner_id: str, owner: Owner):
        doc_ref = owner_collection.document(owner_id)
        doc_ref.set(owner.to_db_format())

    @staticmethod
    def delete_owner(owner_id: str):
        owner_collection.document(owner_id).delete()

    @staticmethod
    def find_by_veterinarian_id(veterinarian_id: str):
        query = owner_collection.where("veterinarian", "==", veterinarian_id).stream()
        owners = [Owner.from_dict_db(doc.to_dict(), doc.id) for doc in query]
        return owners
