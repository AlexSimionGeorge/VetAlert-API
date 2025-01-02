from firebase_admin import storage
import uuid

class FirebaseStorageService:
    @staticmethod
    def upload_animal_picture(file):
        try:
            bucket = storage.bucket()
            blob = bucket.blob(f"animal_picture/{uuid.uuid4()}")
            blob.upload_from_file(file, content_type=file.content_type)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            print("exception: ----------------------------\n", e)
            return ""
