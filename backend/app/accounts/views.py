"""
Authentication API Views for Case Note Management System
"""
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from .models import User


def login_user(request, username: str, password: str):
    """
    Authenticate a user and return JWT tokens.
    """
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return {
            "success": True,
            "message": "Login successful",
            "access_token": str(access_token),
            "refresh_token": str(refresh),
            "user": {
                "id": str(user.id),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "employee_id": user.employee_id,
                "department": user.department
            }
        }
    else:
        return None


def logout_user(request):
    """
    Logout the current user by blacklisting the refresh token.
    """
    try:
        # Get refresh token from request body if provided
        refresh_token = getattr(request, 'refresh_token', None)
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return {
            "success": True,
            "message": "Logout successful"
        }
    except Exception:
        # Even if token blacklisting fails, we can still return success
        # since the client will remove the token
        return {
            "success": True,
            "message": "Logout successful"
        }


def refresh_token(refresh_token_str: str):
    """
    Refresh the access token using a valid refresh token.
    """
    try:
        refresh = RefreshToken(refresh_token_str)
        access_token = refresh.access_token
        
        return {
            "success": True,
            "access_token": str(access_token),
        }
    except Exception:
        return None