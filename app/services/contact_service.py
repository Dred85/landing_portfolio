import logging
import smtplib
import os
from email.message import EmailMessage
from app.schemas.contact import ContactForm

logger = logging.getLogger(__name__)

# Настройки SMTP из переменных окружения
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.rambler.ru")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "adrolv@rambler.ru")
SMTP_PASS = os.getenv("SMTP_PASS", "123456A")
SMTP_TO_EMAIL = os.getenv("SMTP_TO_EMAIL", "adrolv@rambler.ru")

def is_email_disabled() -> bool:
    """
    Проверяет, отключена ли отправка email.
    Динамически читает переменную окружения для поддержки тестов.
    """
    return os.getenv("DISABLE_EMAIL", "false").lower() in ("true", "1", "yes")

async def process_contact_form(form: ContactForm):
    """
    Отправляет email на указанный адрес.
    Если не получается — логирует сообщение.
    
    В режиме DISABLE_EMAIL=true email не отправляется (для тестов).
    """
    # Режим заглушки - не отправляем реальные email
    if is_email_disabled():
        logger.info(f"[ТЕСТОВЫЙ РЕЖИМ] Email не отправлен: {form.model_dump()}")
        return {
            "status": "success", 
            "message": "Сообщение получено (тестовый режим, email не отправлен)"
        }
    
    msg = EmailMessage()
    msg['Subject'] = f"Новое сообщение от {form.name}"
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_TO_EMAIL
    msg.set_content(
        f"Имя: {form.name}\n"
        f"Email: {form.email}\n"
        f"Сообщение:\n{form.message}"
    )

    try:
        # Используем SMTP_SSL для порта 465
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.set_debuglevel(0)  # Отключаем debug после настройки
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        # Используем STARTTLS для порта 587
        else:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.set_debuglevel(0)  # Отключаем debug после настройки
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)

        logger.info(f"Сообщение успешно отправлено: {form.model_dump()}")
        return {"status": "success", "message": "Сообщение отправлено на email!"}

    except Exception as e:
        # Если что-то пошло не так — логируем и возвращаем ошибку
        logger.error(f"Ошибка при отправке письма: {e}")
        logger.info(f"Форма заполнена (email не отправлен): {form.model_dump()}")
        return {"status": "error", "message": f"Не удалось отправить письмо. Ошибка: {str(e)}"}

