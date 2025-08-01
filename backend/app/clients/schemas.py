"""
Client API Schemas
"""
from ninja import Schema
from typing import List


class ClientSearchResponse(Schema):
    id: str
    first_name: str
    last_name: str
    client_id: str


class ClientSearchPaginatedResponse(Schema):
    clients: List[ClientSearchResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ErrorResponse(Schema):
    error: str