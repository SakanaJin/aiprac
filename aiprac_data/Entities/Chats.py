from sqlalchemy import Column, Uuid, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from uuid import uuid7
from datetime import datetime 

from database import Base
from Utils.Time import round_nearest_min
from Entities.dtos import ChatGetDto, ChatShallowDto

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid7)
    name = Column(String(256), nullable=False, default="New Chat")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: round_nearest_min(datetime.now()))
    last_used = Column(DateTime(timezone=True), nullable=False, default=lambda: round_nearest_min(datetime.now()))
    pinned = Column(Boolean, nullable=False, default=False)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    def toGetDto(self) -> ChatGetDto:
        return ChatGetDto(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            last_used=self.last_used,
            pinned=self.pinned,
            messages=[message.toShallowDto() for message in self.messages]
        )
    
    def toShallowDto(self) -> ChatShallowDto:
        return ChatShallowDto(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            last_used=self.last_used,
            pinned=self.pinned
        )