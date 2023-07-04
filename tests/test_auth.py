import pytest
from sqlalchemy import insert, select

from src.auth.models import role
from conftest import client, async_session_maker

# Тест для добавления роли
async def test_add_role():
    # Устанавливаем асинхронное соединение с базой данных
    async with async_session_maker() as session:
        # Создаем выражение для вставки записи о роли в таблицу
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        # Выполняем выражение
        await session.execute(stmt)
        # Фиксируем изменения в базе данных
        await session.commit()

        # Создаем запрос для выборки всех записей из таблицы ролей
        query = select(role)
        # Выполняем запрос
        result = await session.execute(query)
        # Проверяем, что добавленная роль соответствует ожидаемому результату
        assert result.all() == [(1, 'admin', None)], "Роль не добавилась"

# Тест для регистрации
def test_register():
    # Отправляем POST-запрос на регистрацию пользователя
    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    })

    # Проверяем, что статус код ответа равен 201 (Created)
    assert response.status_code == 201
