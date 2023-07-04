from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from auth.manager import get_user_manager
from utils.data import get_date, get_current_user_info
from .models import User
from .base_config import auth_backend, fastapi_users
from .schemas import UserCreate, UserRead
router = APIRouter(
    tags=["Auth"],
)
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
def register(request: Request, year=Depends(get_date), user_info=Depends(get_current_user_info)):
    return templates.TemplateResponse("register.html", {
        "request": request,
        "year": year,
        "user_active": user_info["user_active"],
        "current_username": user_info["current_username"] })

@router.get("/login", response_class=HTMLResponse)
def login(request: Request, year=Depends(get_date), user_info=Depends(get_current_user_info)):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "year": year,
        "user_active": user_info["user_active"],
        "current_username": user_info["current_username"] })

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",    
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",    
    tags=["Auth"],
)

@router.post("/delete-user")
async def delete_user(
    user: User = Depends(fastapi_users.current_user(active=True)),
    user_manager=Depends(get_user_manager),
):
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    # Удаление пользователя из базы данных
    await user_manager.delete(user)

    return JSONResponse(content={"message": "Пользователь успешно удален."})

