from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.Item import Item
from api.repository.ItemRepository import ItemRepository


class ItemView(APIView):
    def get(self, request, item_id=None):
        uid = request.user.to_dict()['uid']

        if item_id:
            item = ItemRepository.get_item(item_id)
            if item and item.veterinarian == uid:
                return Response(item.to_dict(), status=status.HTTP_200_OK)
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = ItemRepository.find_by_veterinarian_id(uid)
            return Response([item.to_dict() for item in items], status=status.HTTP_200_OK)

    def post(self, request):
        uid = request.user.to_dict()['uid']
        try:
            data = request.data
            item = Item.from_post_request(data, uid)
            item = ItemRepository.add_item(item)
            return Response(item.to_dict(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, item_id):
        uid = request.user.to_dict()['uid']

        try:
            data = request.data
            new_item = Item.from_put_request(data)

            old_item = ItemRepository.get_item(item_id)
            if not old_item or old_item.veterinarian != uid:
                return Response({"error": "Can't change items that don't belong to you."}, status=status.HTTP_400_BAD_REQUEST)

            new_item.merge_with(old_item)

            ItemRepository.update_item(item_id, new_item)
            return Response({"message": "Item updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        uid = request.user.to_dict()['uid']

        try:
            item = ItemRepository.get_item(item_id)
            if item and item.veterinarian == uid:
                ItemRepository.delete_item(item_id)
                return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You can't delete non-existent items/items that don't belong to you."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
