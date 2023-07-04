from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pages.router import router as router_pages
from auth.router import router as router_auth
from user_profile.router import router as router_userprofile
from avatars.router import router as router_avatars
from messages.router import router as router_messages

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Travel App"
)

# Монтируем статические файлы для обслуживания
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем роутеры для различных модулей
app.include_router(router_pages)
app.include_router(router_auth)
app.include_router(router_userprofile)
app.include_router(router_avatars)
app.include_router(router_messages)

# Определяем разрешенные источники CORS
origins = [
    "http://localhost:8000",
]

# Добавляем промежуточное ПО CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
