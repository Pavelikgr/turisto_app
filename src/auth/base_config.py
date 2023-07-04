from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from auth.manager import get_user_manager
from auth.models import User
from config import SECRET_AUTH

# Создаем объект CookieTransport для передачи аутентификационных данных через куки
cookie_transport = CookieTransport(cookie_name="travels", cookie_max_age=3600)

# Функция для получения стратегии JWT
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)

# Создаем объект AuthenticationBackend для аутентификации пользователей
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# Создаем экземпляр FastAPIUsers, который обеспечивает CRUD-операции для пользователей
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Получаем текущего пользователя с помощью метода current_user() из fastapi_users
current_user = fastapi_users.current_user()
