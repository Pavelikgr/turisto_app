from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from utils.data import get_date, get_current_user_info


router = APIRouter(
    tags=["Pages"],
)
    
templates = Jinja2Templates(directory="templates")




@router.get("/")
def get_base_page(request: Request, year=Depends(get_date), user_info=Depends(get_current_user_info)):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "year": year,
        "user_active": user_info["user_active"],
        "current_username": user_info["current_username"]   
        })

