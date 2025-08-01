"""
Case Note API Views
"""
from clients.models import Client
from .models import CaseNote
from .schemas import CaseNoteCreateRequest, CaseNoteCreateResponse, CaseNoteResponse, CaseNotesListResponse


def create_case_note(request, payload: CaseNoteCreateRequest):
    """
    Create a new case note for a client.
    Only the assigned caseworker can create notes for their clients.
    """
    # Get the authenticated user from the request
    user = getattr(request, 'auth', None) or getattr(request, 'user', None)
    
    if not user or not user.is_authenticated:
        return None, "Authentication required"
    
    # Get the client and verify assignment
    try:
        client = Client.objects.get(
            id=payload.client_id,
            assigned_caseworker=user
        )
    except (Client.DoesNotExist, ValueError):
        return None, "Client not found or not assigned to you"
    
    # Validate interaction type
    valid_types = [choice[0] for choice in CaseNote.INTERACTION_TYPES]
    if payload.interaction_type not in valid_types:
        return None, f"Invalid interaction type. Must be one of: {', '.join(valid_types)}"
    
    # Create the case note
    case_note = CaseNote.objects.create(
        client=client,
        content=payload.content,
        interaction_type=payload.interaction_type,
        created_by=user
    )
    
    return CaseNoteCreateResponse(
        id=str(case_note.id),
        created_at=case_note.created_at.isoformat(),
        success=True
    ), None


def get_client_case_notes(request, client_id: str):
    """
    Get all case notes for a specific client.
    Only accessible by the assigned caseworker.
    """
    # Get the authenticated user from the request
    user = getattr(request, 'auth', None) or getattr(request, 'user', None)
    
    if not user or not user.is_authenticated:
        return None, "Authentication required"
    
    # Get the client and verify assignment
    try:
        client = Client.objects.get(
            id=client_id,
            assigned_caseworker=user
        )
    except (Client.DoesNotExist, ValueError):
        return None, "Client not found or not assigned to you"
    
    # Get all case notes for this client
    case_notes = CaseNote.objects.filter(client=client).order_by('-created_at')
    
    case_notes_data = [
        CaseNoteResponse(
            id=str(note.id),
            content=note.content,
            interaction_type=note.interaction_type,
            created_at=note.created_at.isoformat(),
            created_by={
                "id": str(note.created_by.id),
                "name": f"{note.created_by.first_name} {note.created_by.last_name}"
            }
        )
        for note in case_notes
    ]
    
    return CaseNotesListResponse(case_notes=case_notes_data), None
