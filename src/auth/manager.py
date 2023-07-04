from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import (BaseUserManager, IntegerIDMixin, exceptions, models,
                           schemas)

from auth.models import User
from auth.utils import get_user_db
from config import SECRET_AUTH

# Определяем класс UserManager, который является менеджером пользователей
class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    # Устанавливаем секретный ключ для сброса пароля и подтверждения пользователя
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(
        self, 
        user: User, 
        request: Optional[Request] = None):
        
        # Выполняем действия после регистрации пользователя, например, выводим информацию о пользователе
        print(f"User {user.id} has registered.")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        # Валидируем пароль пользователя
        await self.validate_password(user_create.password, user_create)

        # Проверяем, существует ли уже пользователь с указанным email
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()
    
        # Создаем словарь с данными пользователя
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        # Создаем пользователя в базе данных
        created_user = await self.user_db.create(user_dict)

        # Выполняем действия после регистрации пользователя
        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        print(f"User {user.id} logged in.")
    

# Функция для получения экземпляра UserManager
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
