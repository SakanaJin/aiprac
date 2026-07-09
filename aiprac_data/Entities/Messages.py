from sqlalchemy import Column, Uuid, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid7
from datetime import datetime

from database import Base
from Utils.Time import round_nearest_min
from Utils.Role import Role
from Entities.dtos import MessageGetDto, MessageShallowDto

class Message(Base):
    __tablename__ = "messages"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid7)
    content = Column(Text, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.CLANKER)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: round_nearest_min(datetime.now()))

    chatid = Column(Uuid(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"))
    chat = relationship("Chat", back_populates="messages")

    def toGetDto(self) -> MessageGetDto:
        return MessageGetDto(
            id=self.id,
            content=self.content,
            role=self.role,
            created_at=self.created_at,
            chat=self.chat.toShallowDto()
        )
    
    def toShallowDto(self) -> MessageShallowDto:
        return MessageShallowDto(
            id=self.id,
            content=self.content,
            role=self.role,
            created_at=self.created_at
        )