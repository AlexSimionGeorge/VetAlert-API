from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.Animal import Animal
from api.repository.AnimalRepository import AnimalRepository


class AnimalView(APIView):
    def get(self, request, animal_id=None):
        uid = request.user.to_dict()['uid']

        if animal_id:
            animal = AnimalRepository.get_animal(animal_id)
            if animal and animal.veterinarian == uid:
                return Response(animal.to_dict(), status=status.HTTP_200_OK)
            return Response({"error": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            animals = AnimalRepository.find_by_veterinarian_id(uid)
            return Response([animal.to_dict() for animal in animals], status=status.HTTP_200_OK)

    def post(self, request):
        uid = request.user.to_dict()['uid']
        try:
            data = request.data
            animal = Animal.from_post_request(data, uid)
            animal = AnimalRepository.add_animal(animal)
            return Response(animal.to_dict(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, animal_id):
        uid = request.user.to_dict()['uid']

        try:
            data = request.data
            new_animal = Animal.from_put_request(data)

            old_animal = AnimalRepository.get_animal(animal_id)
            if not old_animal or old_animal.veterinarian != uid:
                return Response({"error": "Can't change animals that don't belong to you."}, status=status.HTTP_400_BAD_REQUEST)

            new_animal.merge_with(old_animal)

            AnimalRepository.update_animal(animal_id, new_animal)
            return Response({"message": "Animal updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, animal_id):
        uid = request.user.to_dict()['uid']

        try:
            animal = AnimalRepository.get_animal(animal_id)
            if animal and animal.veterinarian == uid:
                AnimalRepository.delete_animal(animal_id)
                return Response({"message": "Animal deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You can't delete non-existent animal/ animal that doesn't belong to you."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

