from django.http import JsonResponse
from firebase_admin import auth
from django.utils.deprecation import MiddlewareMixin

from api.models.FirebaseAuthUser import FirebaseAuthUser

class AuthFirewall(MiddlewareMixin):
    def process_request(self, request):
        """
        This method is called on each request before the view (and other middleware).
        """
        if not request.path.startswith('/api/'):
            return

        if not hasattr(request, '_dont_enforce_csrf_checks'):
            request._dont_enforce_csrf_checks = True

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "Unauthorized: No token"}, status=401)

        try:
            token = auth_header.split(" ")[1]
            decoded_token = auth.verify_id_token(token)

            request.user = FirebaseAuthUser(
                uid=decoded_token['uid'],
                name=decoded_token.get('name'),
                email=decoded_token.get('email'),
            )
        except Exception as e:
            return JsonResponse({"error": "Unauthorized: Invalid token"}, status=401)


    def process_response(self, request, response):
        """
        This method is called on each response before it is returned to the client.
        """
        return response
