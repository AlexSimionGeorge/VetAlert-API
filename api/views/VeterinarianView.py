from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.Veterinarian import Veterinarian
from api.repository.VeterinarianRepository import VeterinarianRepository


class VeterinarianView(APIView):
    def post(self, request):
        try:

            user = request.user
            uid = user.to_dict()['uid']
            name = user.to_dict()['name']
            email = user.to_dict()['email']

            cabinet_address = request.data.get('cabinetAddress')
            phone_number = request.data.get('phoneNumber')

            veterinarian = Veterinarian(name=name, email=email, cabinet_address=cabinet_address, phone_number=phone_number)
            VeterinarianRepository.create_veterinarian(uid, veterinarian)

            return Response({"message": "Veterinarian updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
