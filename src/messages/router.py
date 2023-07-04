from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, or_, select

from auth.models import User
from database import get_async_session
from messages.models import Message
from messages.schemas import MessageCreate
from utils.data import get_current_user_info, get_user_info, get_date

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
    )
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def message(
    request: Request,
    year=Depends(get_date),
    current_user_info=Depends(get_current_user_info),
    session=Depends(get_async_session),
):
    current_profile_id = current_user_info["current_profile_id"]

    # Выполняем запрос к таблице message
    query = select(Message).where(
        or_(Message.sender_id == current_profile_id, Message.recipient_id == current_profile_id)
    ).order_by(Message.created_at.desc())
    result = await session.execute(query)
    messages = result.scalars().all()

    # Получаем список чужих пользователей
    other_users = []
    for message in messages:
        if message.sender_id != current_profile_id and message.sender_id not in other_users:
            other_users.append(message.sender_id)
        if message.recipient_id != current_profile_id and message.recipient_id not in other_users:
            other_users.append(message.recipient_id)

    # Получаем имена пользователей
    users_info = []
    for user_id in other_users:
        user_info = await get_user_info(user_id, session)
        users_info.append(user_info["profile_username"])

    return templates.TemplateResponse(
        "messages.html",
        {
            "request": request,
            "year": year,
            "user_active": True,
            "current_username": current_user_info["current_username"],
            "current_profile_id": current_user_info["current_profile_id"],
            "users": users_info,
        },
    )


    
@router.post("/")
async def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_user_info),
    session=Depends(get_async_session)
):
    # Получаем отправителя и получателя по их ID
    sender = await session.get(User, current_user["current_profile_id"])
    recipient = await session.get(User, message.recipient_id)

    # Создаем новое сообщение и связываем его с отправителем и получателем
    new_message = Message(
        sender_id=sender.id,
        recipient_id=recipient.id,
        content=message.content
    )
    session.add(new_message)
    await session.commit()

    return {"message": "Message sent successfully"}


@router.get("/{message_id}")
async def get_message(message_id: int, session=Depends(get_async_session)):
    # Получаем сообщение по его ID
    message = await session.get(Message, message_id)
    return message
@router.get("/history")
async def get_message_history(
    recipient_id: int,
    current_user_info=Depends(get_current_user_info),
    session=Depends(get_async_session),
):
    current_profile_id = current_user_info["current_profile_id"]

    query = select(Message).where(
        or_(
            and_(Message.sender_id == current_profile_id, Message.recipient_id == recipient_id),
            and_(Message.sender_id == recipient_id, Message.recipient_id == current_profile_id),
        )
    ).order_by(Message.created_at.asc())

    result = await session.execute(query)
    messages = result.scalars().all()

    return {"messages": messages}
