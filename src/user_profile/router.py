from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from utils.data import get_date, get_user_info, get_current_user_info
from avatars.router import router as avatars_router 

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/{profile_id}", response_class=HTMLResponse)
def get_profile_by_id(
    request: Request,
    profile_id: int,
    year=Depends(get_date),
    current_user_info=Depends(get_current_user_info),
    profile_user_info=Depends(get_user_info),
):
    if not current_user_info["current_username"]:
        # Перенаправляем пользователя на страницу регистрации
        return RedirectResponse(url="/login")

    avatar_url = avatars_router.url_path_for(
        "update_avatar", username=profile_user_info["profile_username"]
    )

    if profile_user_info["profile_username"] is None:
        # Обработка случая, когда пользователь с указанным profile_id не найден
        return RedirectResponse(url="/")  # Перенаправляем на другую страницу или выводим сообщение об ошибке

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "year": year,
            "user_active": True,
            "current_username": current_user_info["current_username"],
            "profile_username": profile_user_info["profile_username"],            
            "avatar_url": avatar_url,
            "profile_id": profile_id,
        },
    )




@router.get("/", response_class=HTMLResponse)
def get_profile(
    request: Request,
    year=Depends(get_date),
    current_user_info=Depends(get_current_user_info),
):
    if not current_user_info["current_username"]:
        # Перенаправляем пользователя на страницу регистрации
        return RedirectResponse(url="/login")

    if current_user_info["current_profile_id"] is not None:
        return RedirectResponse(
            url=f"/profile/{current_user_info['current_profile_id']}"
        )

    return RedirectResponse(url="/")

