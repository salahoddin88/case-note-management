"""
Authentication API Schemas
"""
from ninja import Schema
from typing import Optional


class LoginRequest(Schema):
    username: str
    password: str


class LoginResponse(Schema):
    success: bool
    message: str
    access_token: str
    refresh_token: str
    user: dict


class LogoutRequest(Schema):
    refresh_token: Optional[str] = None


class LogoutResponse(Schema):
    success: bool
    message: str


class RefreshTokenRequest(Schema):
    refresh_token: str


class RefreshTokenResponse(Schema):
    success: bool
    access_token: str


class ErrorResponse(Schema):
    error: str