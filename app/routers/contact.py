from fastapi import APIRouter
from app.schemas.contact import ContactForm
from app.services.contact_service import process_contact_form

router = APIRouter(prefix="/api")

@router.post("/contact")
async def contact(form: ContactForm):
    return await process_contact_form(form)
