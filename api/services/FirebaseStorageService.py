from urllib.parse import urlparse

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
        """
        Deletes an image from Firebase Storage.

        :param image_url: The public URL of the image to delete.
        :return: None
        """
        imag_id = image_url.split("/")[-1]
        try:
            bucket = storage.bucket()
            blob = bucket.blob('animal_picture/' + imag_id)
            blob.delete()  # Delete the file
        except Exception as e:
            print(f"\n\n\n\nError deleting image {imag_id} ___________________________________________:\n{str(e)}")

