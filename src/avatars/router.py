import os
from fastapi import APIRouter, FastAPI, File, HTTPException, Request, UploadFile
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from .avatar_storage import AvatarStorage
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from utils.data import get_date, get_user_info
from fastapi.staticfiles import StaticFiles

app = FastAPI()
router = APIRouter(
    tags=["Avatar"]
)

templates = Jinja2Templates(directory="templates")


storage_directory = os.path.join(os.getcwd(), "storage/avatar/")
storage = AvatarStorage(storage_directory=storage_directory)

app.mount("/avatars", StaticFiles(directory="storage/avatar/"), name="avatars")

@router.put("/users/{username}/avatar")
async def update_avatar(username: str, file: UploadFile = File(...)):
    # Проверяем существование пользователя и выполняем другую логику
    # ...

    avatar_filename = f"{username}.png"
    avatar_path = os.path.join(storage_directory, avatar_filename)

    # Удаляем старую аватарку, если она существует
    if os.path.exists(avatar_path):
        os.remove(avatar_path)

    # Сохраняем новую аватарку
    with open(avatar_path, "wb") as f:
        f.write(await file.read())

    return {"message": "Avatar updated successfully"}

@router.get("/users/{username}/avatar", response_class=FileResponse)
async def get_avatar(username: str):
    avatar_filename = f"{username}.png"
    avatar_path = os.path.join(storage_directory, avatar_filename)
    if not os.path.exists(avatar_path):
        raise HTTPException(status_code=404, detail="Avatar not found")
    return avatar_path

@router.delete("/users/{username}/avatar")
async def delete_avatar(username: str):
    avatar_filename = f"{username}.png"
    storage.delete_avatar(avatar_filename)
    return {"message": "Avatar deleted successfully"}