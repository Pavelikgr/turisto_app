from fastapi import APIRouter, Depends
from auth.models import User
from database import get_async_session
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from auth.base_config import fastapi_users

# Определяем зависимость для текущего активного верифицированного пользователя (необязательная зависимость)
optional_current_active_verified_user = fastapi_users.current_user(active=True, optional=True)

# Функция для получения текущего года
def get_date():
    year = datetime.datetime.now().year
    return year

# Функция для получения информации о текущем пользователе
def get_current_user_info(user: User = Depends(optional_current_active_verified_user)):
    if user is None:
        return {"user_active": False, "current_username": None, "current_profile_id": None}
    else:
        return {"user_active": True, "current_username": user.username, "current_profile_id": user.id}

# Асинхронная функция для получения информации о пользователе по ID профиля
async def get_user_info(profile_id: int, session: AsyncSession = Depends(get_async_session)):
    profile_user = await session.get(User, profile_id)
    profile_username = profile_user.username if profile_user else None

    return {"profile_username": profile_username}
