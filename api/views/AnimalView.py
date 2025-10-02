from pprint import pprint

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.Animal import Animal
from api.repository.AnimalRepository import AnimalRepository
from api.services.FirebaseStorageService import FirebaseStorageService


class AnimalView(APIView):
    def get(self, request, animal_id=None):
        uid = request.user.to_dict()['uid']

        if animal_id:
            animal = AnimalRepository.get_animal(animal_id)
            if animal and animal.veterinarian == uid:
                return Response(animal.to_response(), status=status.HTTP_200_OK)
            return Response({"error": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            animals = AnimalRepository.find_by_veterinarian_id(uid)
            return Response([animal.to_response() for animal in animals], status=status.HTTP_200_OK)

    def post(self, request):
        uid = request.user.to_dict()['uid']
        try:
            data = request.data

            picture = request.FILES.get('picture')
            if picture:
                picture_url = FirebaseStorageService.upload_animal_picture(picture)
            else:
                return Response({"error": "Picture file is required"}, status=status.HTTP_400_BAD_REQUEST)

            animal = Animal.from_post_request(data, uid, picture_url)
            animal = AnimalRepository.add_animal(animal)
            return Response(animal.to_response(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, animal_id):
        uid = request.user.to_dict()['uid']
        old_animal = AnimalRepository.get_animal(animal_id)
        if not old_animal or old_animal.veterinarian != uid:
            return Response({"error": "Can't change animals that don't belong to you."},
                            status=status.HTTP_400_BAD_REQUEST)

        new_pic = False
        try:
            picture = request.FILES.get('picture')
            if picture:
                picture_url = FirebaseStorageService.upload_animal_picture(picture)
                if old_animal.picture is not None:
                    FirebaseStorageService.delete_animal_picture(old_animal.picture)
                new_pic = True
            else:
                picture_url = None

            data = request.data
            new_animal = Animal.from_put_request(data, picture_url)

            new_animal.merge_with(old_animal)
            if new_pic:
                new_animal.picture = picture_url
            AnimalRepository.update_animal(animal_id, new_animal)
            return Response(new_animal.to_response(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, animal_id):
        uid = request.user.to_dict()['uid']

        try:
            animal = AnimalRepository.get_animal(animal_id)
            if animal and animal.veterinarian == uid:
                if animal.picture is not None:
                    FirebaseStorageService.delete_animal_picture(animal.picture)
                AnimalRepository.delete_animal(animal_id)
                return Response({"message": "Animal deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You can't delete non-existent animal/ animal that doesn't belong to you."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

