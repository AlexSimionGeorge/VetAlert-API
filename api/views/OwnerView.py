from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.Owner import Owner
from api.repository.OwnerRepository import OwnerRepository


class OwnerView(APIView):
    def get(self, request, owner_id=None):
        uid = request.user.to_dict()['uid']
        if owner_id:
            owner = OwnerRepository.get_owner(owner_id)
            if owner and owner.veterinarian == uid:
                return Response(owner.to_dict(), status=status.HTTP_200_OK)
            return Response({"error": "Owner not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            owners = OwnerRepository.find_by_veterinarian_id(uid)
            return Response([owner.to_dict() for owner in owners], status=status.HTTP_200_OK)

    def post(self, request):
        uid = request.user.to_dict()['uid']
        try:
            data = request.data
            owner = Owner.from_post_request(data, uid)
            owner = OwnerRepository.add_owner(owner)
            return Response(owner.to_dict(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, owner_id):
        uid = request.user.to_dict()['uid']

        try:
            data = request.data
            new_owner = Owner.from_put_request(data)

            old_owner = OwnerRepository.get_owner(owner_id)
            if not old_owner or old_owner.veterinarian != uid:
                return Response({"error": "Can't change owners that don't belong to you."}, status=status.HTTP_404_NOT_FOUND)

            new_owner.merge_with(old_owner)

            OwnerRepository.update_owner(owner_id, new_owner)
            return Response({"message": "Owner updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, owner_id):
        uid = request.user.to_dict()['uid']
        try:
            owner = OwnerRepository.get_owner(owner_id)
            if owner and owner.veterinarian == uid:
                OwnerRepository.delete_owner(owner_id)
                return Response({"message": "Owner deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Owner not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
