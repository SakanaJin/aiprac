from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc, func
from sqlalchemy.orm import Session

from database import get_db
from Utils.Response import Response, HttpException
from Entities.Chats import Chat
from Entities.dtos import ChatUpdateDto, PaginationDto, PageDto

router = APIRouter(prefix="/api/chats", tags=["Chats"])

PAGE_SIZE = 10 # chat previews

@router.get("")
def get_all(db: Session = Depends(get_db)):
    response = Response()
    chats = db.scalars(
        select(Chat)
    ).all()
    response.data = [chat.toGetDto() for chat in chats]
    return response

@router.post("")
def create(db: Session = Depends(get_db)):
    response = Response()
    chat = Chat()
    db.add(chat)
    db.commit()
    response.data = chat.toGetDto()
    return response

@router.get("/{id}")
def get_byid(id: int, db: Session = Depends(get_db)):
    response = Response()
    chat = db.get(Chat, id)
    if not chat:
        response.add_error("id", "chat not found")
        raise HttpException(status_code=404, response=response)
    response.data = chat.toGetDto()
    return response

@router.patch("/{id}")
def update(chatdto: ChatUpdateDto, id: int, db: Session = Depends(get_db)):
    response = Response()
    chat = db.get(Chat, id)
    if len(chatdto.name) == 0:
        response.add_error("name", "name cannot be empty")
        raise HttpException(status_code=400, response=response)
    if not chat:
        response.add_error("id", "chat not found")
        raise HttpException(status_code=404, response=response)
    chat.name = chatdto.name
    db.commit()
    response.data = chat.toGetDto()
    return response

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    response = Response()
    chat = db.get(Chat, id)
    if not chat:
        response.add_error("id", "chat not found")
        raise HttpException(status_code=404, response=response)
    db.delete(chat)
    db.commit()
    response.data = True
    return response

@router.post("/{id}")
def togglepin(id: int, db: Session = Depends(get_db)):
    response = Response() 
    chat = db.get(Chat, id)
    if not chat:
        response.add_error("id", "chat not found")
        raise HttpException(status_code=404, response=response)
    chat.pinned = not chat.pinned
    db.commit()
    response.data = chat.toGetDto()
    return response

@router.get("/preview")
def get_page(id: int, pagenum: int = Query(default=1, ge=1), pinned: bool = Query(default=False), db: Session = Depends(get_db)):
    response = Response()
    offset = (pagenum - 1) * PAGE_SIZE
    chats = db.scalars(
        select(Chat)
        .where(Chat.pinned == pinned)
        .order_by(desc(Chat.last_used))
        .offset(offset)
        .limit(PAGE_SIZE)
    ).all()
    total_chats = db.scalars(
        select(func.count(Chat.id))
        .where(Chat.pinned == pinned)
    )
    total_pages = -(-total_chats // PAGE_SIZE)
    pagination = PaginationDto(
        current_page=pagenum,
        total_pages=total_pages,
        total_items=total_chats,
        page_size=PAGE_SIZE,
        has_more=pagenum < total_pages
    )
    response.data = PageDto(
        items=[chat.toShallowDto() for chat in chats],
        pagination=pagination
    )
    return response

@router.get("/search")
def search_chats(name: str = Query(..., min_length=1, max_length=256), limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    response = Response()
    chats = db.scalars(
        select(Chat)
        .where(Chat.name.like(f"%{name}%"))
        .limit(limit)
    ).all()
    response.data = [chat.toShallowDto() for chat in chats]
    return response