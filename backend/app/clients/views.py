"""
Client API Views
"""
from django.db.models import Q
from .models import Client
from .schemas import ClientSearchResponse


def search_clients(request, q: str = "", page: int = 1, page_size: int = 10):
    """
    Search for clients by name or client ID with pagination.
    Only returns clients assigned to the authenticated caseworker.
    """
    # Get the authenticated user from the request
    # In Django Ninja with JWT, the user is set by the auth handler
    user = getattr(request, 'auth', None) or getattr(request, 'user', None)
    
    if not user or not user.is_authenticated:
        return {
            "clients": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0
        }
    
    # Search by name or client_id, but only for assigned clients
    query = Q(assigned_caseworker=user)
    
    if q:
        query &= (
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(client_id__icontains=q)
        )
    
    # Get total count for pagination
    total_clients = Client.objects.filter(query).count()
    
    # Calculate pagination
    offset = (page - 1) * page_size
    clients = Client.objects.filter(query)[offset:offset + page_size]
    
    # Calculate total pages
    total_pages = (total_clients + page_size - 1) // page_size
    
    client_list = [
        ClientSearchResponse(
            id=str(client.id),
            first_name=client.first_name,
            last_name=client.last_name,
            client_id=client.client_id
        )
        for client in clients
    ]
    
    return {
        "clients": client_list,
        "total": total_clients,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
