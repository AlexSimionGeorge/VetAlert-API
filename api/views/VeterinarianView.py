from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth

from api.models.Veterinarian import Veterinarian
from api.repository.VeterinarianRepository import VeterinarianRepository


class VeterinarianView(APIView):
    def post(self, request):
        try:
            token = request.data.get('idToken')
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            name = decoded_token.get('name')
            email = decoded_token.get('firebase').get('identities').get('email')

            VeterinarianRepository.veterinarian_exists(uid)

            cabinet_address = request.data.get('cabinetAddress')
            phone_number = request.data.get('phoneNumber')

            veterinarian = Veterinarian(name=name, email=email, cabinet_address=cabinet_address, phone_number=phone_number)
            VeterinarianRepository.create_veterinarian(uid, veterinarian)

            return Response({"message": "Veterinarian created successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
