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
            print("\n\n\n\nexception: ----------------------------\n", e)
            return ""

    @staticmethod
    def delete_animal_picture(image_url: str):
        try:
            # Extrage calea completă după numele bucketului
            # Ex: /vetalert-496e7.firebasestorage.app/animal_picture/<uuid>
            path = image_url.split("/", 4)[-1]  # animal_picture/<uuid>

            bucket = storage.bucket()
            blob = bucket.blob(path)
            blob.delete()
        except Exception as e:
            print(f"Error deleting image {image_url}: {str(e)}")
