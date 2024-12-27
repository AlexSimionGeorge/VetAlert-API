from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import auth
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings

db = settings.FIRESTORE_DB  # Correct Firestore client reference

@api_view(['POST'])
def google_login(request):
    token = request.data.get('idToken')
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        # You can retrieve more user info here or create user in Firestore
        user_data = {"uid": uid, "email": decoded_token.get("email")}
        return Response({"message": "User authenticated", "user": user_data})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

class VeterinarianView(APIView):
    def get(self, request, pk=None):
        if pk:  # If a specific document ID is provided
            doc_ref = db.collection('veterinarians').document(pk)
            doc = doc_ref.get()
            if doc.exists:
                return Response(doc.to_dict())  # Return the document data
            else:
                return Response({"error": "Veterinarian not found"}, status=404)
        else:  # If no document ID is provided, fetch all veterinarians
            docs = db.collection('veterinarians').stream()
            veterinarians = [{**doc.to_dict(), "id": doc.id} for doc in docs]
            return Response(veterinarians)

    def post(self, request):
        data = request.data
        db.collection('veterinarians').add(data)
        return Response({"message": "Veterinarian added successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        data = request.data
        doc_ref = db.collection('veterinarians').document(pk)
        doc_ref.update(data)
        return Response({"message": "Veterinarian updated successfully"})

    def delete(self, request, pk):
        db.collection('veterinarians').document(pk).delete()
        return Response({"message": "Veterinarian deleted successfully"})


class AnimalView(APIView):
    def get(self, request):
        docs = db.collection('animals').stream()
        animals = [doc.to_dict() for doc in docs]
        return Response(animals)

    def post(self, request):
        data = request.data
        db.collection('animals').add(data)
        return Response({"message": "Animal added successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        data = request.data
        doc_ref = db.collection('animals').document(pk)
        doc_ref.update(data)
        return Response({"message": "Animal updated successfully"})

    def delete(self, request, pk):
        db.collection('animals').document(pk).delete()
        return Response({"message": "Animal deleted successfully"})
