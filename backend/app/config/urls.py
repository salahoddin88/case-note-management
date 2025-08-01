"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.urls import path
from django.contrib import admin
from ninja import NinjaAPI
from typing import List
from config.auth import JWTAuth

# Import views directly from each app
from accounts.views import login_user, logout_user, refresh_token
from accounts.schemas import (
    LoginRequest, LoginResponse, LogoutRequest, LogoutResponse,
    RefreshTokenRequest, RefreshTokenResponse, ErrorResponse
)
from clients.views import search_clients
from clients.schemas import ClientSearchResponse, ClientSearchPaginatedResponse
from case_notes.views import create_case_note, get_client_case_notes
from case_notes.schemas import (
    CaseNoteCreateRequest, CaseNoteCreateResponse, 
    CaseNotesListResponse, CaseNoteResponse
)

# Create main API instance with JWT authentication
api = NinjaAPI(title="Case Note Management API", version="1.0.0", auth=JWTAuth())

# Authentication endpoints (no auth required)
@api.post("/auth/login", response={200: LoginResponse, 401: ErrorResponse}, auth=None)
def auth_login(request, payload: LoginRequest):
    result = login_user(request, payload.username, payload.password)
    if result:
        return result
    else:
        return 401, {"error": "Invalid credentials"}

@api.post("/auth/logout", response=LogoutResponse, auth=None)
def auth_logout(request, payload: LogoutRequest = None):
    if payload and payload.refresh_token:
        request.refresh_token = payload.refresh_token
    return logout_user(request)

@api.post("/auth/refresh", response={200: RefreshTokenResponse, 401: ErrorResponse}, auth=None)
def auth_refresh(request, payload: RefreshTokenRequest):
    result = refresh_token(payload.refresh_token)
    if result:
        return result
    else:
        return 401, {"error": "Invalid refresh token"}

# Client endpoints (JWT auth required)
@api.get("/clients/search", response=ClientSearchPaginatedResponse)
def client_search(request, q: str = "", page: int = 1, page_size: int = 10):
    return search_clients(request, q, page, page_size)

# Case note endpoints (JWT auth required)
@api.post("/case-notes/", response={200: CaseNoteCreateResponse, 400: ErrorResponse, 404: ErrorResponse})
def case_note_create(request, payload: CaseNoteCreateRequest):
    result, error = create_case_note(request, payload)
    if result:
        return result
    elif "not found" in error:
        return 404, {"error": error}
    else:
        return 400, {"error": error}

@api.get("/case-notes/client/{client_id}", response={200: CaseNotesListResponse, 404: ErrorResponse})
def case_note_list(request, client_id: str):
    result, error = get_client_case_notes(request, client_id)
    if result:
        return result
    else:
        return 404, {"error": error}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
