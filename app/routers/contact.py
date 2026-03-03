from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import os

from app.schemas.contact import ContactForm
from app.services.contact_service import process_contact_form

router = APIRouter()

# Настройка шаблонов
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# GET /contact - отображение страницы с формой
@router.get("/contact", response_class=HTMLResponse)
async def get_contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

# POST /contact - обработка формы со страницы
@router.post("/contact", response_class=HTMLResponse)
async def post_contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Создаём объект ContactForm из данных формы
    form = ContactForm(name=name, email=email, message=message)
    result = await process_contact_form(form)
    
    # Рендерим страницу с результатом
    if result["status"] == "success":
        return templates.TemplateResponse(
            "contact.html", 
            {"request": request, "success": True}
        )
    else:
        return templates.TemplateResponse(
            "contact.html", 
            {"request": request, "error": result["message"]}
        )

# POST /api/contact - JSON API endpoint (для программных запросов)
@router.post("/api/contact")
async def contact_api(form: ContactForm):
    return await process_contact_form(form)
