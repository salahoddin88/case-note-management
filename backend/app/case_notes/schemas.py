"""
Case Note API Schemas
"""
from ninja import Schema
from typing import List


class CaseNoteCreateRequest(Schema):
    client_id: str
    content: str
    interaction_type: str = "other"


class CaseNoteResponse(Schema):
    id: str
    content: str
    interaction_type: str
    created_at: str
    created_by: dict


class CaseNoteCreateResponse(Schema):
    id: str
    created_at: str
    success: bool


class CaseNotesListResponse(Schema):
    case_notes: List[CaseNoteResponse]


class ErrorResponse(Schema):
    error: str