from firebase_admin import firestore
from api.models.Item import Item
from api.repository.CollectionsConfig import ItemCollection

item_collection = firestore.client().collection(ItemCollection)

class ItemRepository:
    @staticmethod
    def add_item(item: Item):
        doc_ref = item_collection.document()
        doc_ref.set(item.to_db_format())
        item.iid = doc_ref.id
        return item

    @staticmethod
    def get_item(item_id: str):
        doc = item_collection.document(item_id).get()
        if doc.exists:
            return Item.from_dict_db(doc.to_dict(), doc.id)
        return None

    @staticmethod
    def update_item(item_id: str, item: Item):
        doc_ref = item_collection.document(item_id)
        doc_ref.set(item.to_db_format())

    @staticmethod
    def delete_item(item_id: str):
        item_collection.document(item_id).delete()

    @staticmethod
    def find_by_veterinarian_id(veterinarian_id: str):
        query = item_collection.where("veterinarian", "==", veterinarian_id).stream()
        items = [Item.from_dict_db(doc.to_dict(), doc.id) for doc in query]
        return items
