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

async def process_contact_form(form: ContactForm):
    """
    Отправляет email на указанный адрес.
    Если не получается — логирует сообщение.
    """
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
        # Подключаемся к SMTP через SSL (порт 465)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.set_debuglevel(0)  # Отключаем debug после настройки
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        logger.info(f"Сообщение успешно отправлено: {form.dict()}")
        return {"status": "success", "message": "Сообщение отправлено на email!"}

    except Exception as e:
        # Если что-то пошло не так — логируем и возвращаем ошибку
        logger.error(f"Ошибка при отправке письма: {e}")
        logger.info(f"Форма заполнена (email не отправлен): {form.dict()}")
        return {"status": "error", "message": f"Не удалось отправить письмо. Ошибка: {str(e)}"}

