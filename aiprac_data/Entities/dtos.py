from pydantic import BaseModel
from datetime import datetime
from typing import List
from uuid import UUID

from Utils.Role import Role

#Chat
class ChatGetDto(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    last_used: datetime
    pinned: bool
    messages: List[MessageShallowDto]

class ChatShallowDto(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    last_used: datetime
    pinned: bool

class ChatUpdateDto(BaseModel):
    name: str

#Message
class MessageGetDto(BaseModel):
    id: UUID
    content: str
    role: Role
    created_at: datetime
    chat: ChatShallowDto

class MessageShallowDto(BaseModel):
    id: UUID
    content: str
    role: Role
    created_at: datetime

class MessageCreateDto(BaseModel):
    content: str

#Pagination
class PaginationDto(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    page_size: int
    has_more: bool

class PageDto(BaseModel):
    items: List[object]
    pagination: PaginationDto