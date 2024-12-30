from firebase_admin import auth
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from api.models.FirebaseAuthUser import FirebaseAuthUser

class AuthFirewall(MiddlewareMixin):
    def process_request(self, request):
        if not request.path.startswith('/api/'):
            return

        if not hasattr(request, '_dont_enforce_csrf_checks'):
            request._dont_enforce_csrf_checks = True

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "Unauthorized: No token"}, status=401)

        try:
            token = auth_header.split(" ")[1]
            # Allow for clock skew of up to 10 seconds
            decoded_token = auth.verify_id_token(token, clock_skew_seconds=10)

            request.user = FirebaseAuthUser(
                uid=decoded_token['uid'],
                name=decoded_token.get('name'),
                email=decoded_token.get('email'),
            )
        except Exception as e:
            import traceback
            print("Error verifying token:\n", traceback.format_exc())
            return JsonResponse({"error": "Unauthorized: Invalid token", "details": str(e)}, status=401)
