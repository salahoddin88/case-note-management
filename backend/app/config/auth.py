from ninja.security import HttpBearer
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


class JWTAuth(HttpBearer):
    """JWT Authentication for Django Ninja"""
    
    def authenticate(self, request, token):
        try:
            # Validate the JWT token
            validated_token = AccessToken(token)
            user_id = validated_token['user_id']
            user = User.objects.get(id=user_id)
            return user
        except (InvalidToken, TokenError, User.DoesNotExist):
            return None


class SessionAuth(HttpBearer):
    def authenticate(self, request, token):
        # For session-based auth, we'll check if the user is authenticated
        # This is a simplified approach - in production you'd want more robust session handling
        if hasattr(request, 'user') and request.user.is_authenticated:
            return request.user
        return None


def get_authenticated_user(request):
    """Helper function to get the authenticated user from the request"""
    if hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    return None


# Simple session-based authentication that doesn't require a token
class SessionAuthSimple:
    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            return request.user
        return None