from typing import Optional, List

from fastapi_users import schemas

from messages.schemas import MessageRead

class UserRead(schemas.BaseUser[int]):
    # Определяем класс UserRead, основанный на BaseUser с типом идентификатора int
    id: int
    email: str
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    sent_messages: Optional[List[MessageRead]] = []
    received_messages: Optional[List[MessageRead]] = []

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    # Определяем класс UserCreate, основанный на BaseUserCreate
    username: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
