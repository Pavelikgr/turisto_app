from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    recipient_id: int


class MessageUpdate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    created_at: datetime

    class Config:
        orm_mode = True
