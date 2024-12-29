from firebase_admin import firestore
from api.models.TreatmentLog import TreatmentLog
from api.repository.CollectionsConfig import TreatmentLogCollection, AnimalCollection, ItemCollection

treatment_log_collection = firestore.client().collection(TreatmentLogCollection)
animal_collection = firestore.client().collection(AnimalCollection)
item_collection = firestore.client().collection(ItemCollection)

class TreatmentLogRepository:
    @staticmethod
    def add_treatment_log(treatment_log: TreatmentLog):
        doc_ref = treatment_log_collection.document()
        doc_ref.set(treatment_log.to_db_format())
        treatment_log.tlid = doc_ref.id
        return treatment_log

    @staticmethod
    def get_treatment_log(tlid: str):
        doc = treatment_log_collection.document(tlid).get()
        if doc.exists:
            return TreatmentLog.from_dict_db(doc.to_dict(), doc.id)
        return None

    @staticmethod
    def update_treatment_log(tlid: str, treatment_log: TreatmentLog):
        doc_ref = treatment_log_collection.document(tlid)
        doc_ref.set(treatment_log.to_db_format())

    @staticmethod
    def delete_treatment_log(tlid: str):
        treatment_log_collection.document(tlid).delete()

    @staticmethod
    def find_by_veterinarian_id(veterinarian_id: str):
        animal_ids = animal_collection.where("veterinarian", "==", veterinarian_id).select(["__name__"]).stream()
        animal_id_list = [doc.id for doc in animal_ids]

        item_ids = item_collection.where("veterinarian", "==", veterinarian_id).select(["__name__"]).stream()
        item_id_list = [doc.id for doc in item_ids]

        treatment_logs_query = treatment_log_collection \
            .where("animal", "in", animal_id_list) \
            .where("item", "in", item_id_list) \
            .stream()

        treatment_logs = [TreatmentLog.from_dict_db(doc.to_dict(), doc.id) for doc in treatment_logs_query]

        return treatment_logs

    @staticmethod
    def is_valid_animal(animal_id: str, veterinarian_id: str):
        doc = animal_collection.document(animal_id).get()
        return doc.exists and doc.to_dict().get('veterinarian') == veterinarian_id

    @staticmethod
    def is_valid_item(item_id: str, veterinarian_id: str):
        doc = item_collection.document(item_id).get()
        return doc.exists and doc.to_dict().get('veterinarian') == veterinarian_id
