import logging
import logging
import smtplib
from email.message import EmailMessage
from app.schemas.contact import ContactForm

logger = logging.getLogger(__name__)

# Настройки SMTP (можно подставить свои)
SMTP_SERVER = "smtp.rambler.ru"    # SMTP-сервер твоего почтового провайдера
SMTP_PORT = 587                     # Обычно 587 для TLS
SMTP_USER = "adrolv08111985@gmail.com"  # Твой email
SMTP_PASS = "your_app_password"      # Пароль или app password

async def process_contact_form(form: ContactForm):
    """
    Отправляет email на указанный адрес.
    Если не получается — логирует сообщение.
    """
    msg = EmailMessage()
    msg['Subject'] = f"Новое сообщение от {form.name}"
    msg['From'] = SMTP_USER
    msg['To'] = "adrolv@rambler.ru"  # куда реально отправляем
    msg.set_content(
        f"Имя: {form.name}\n"
        f"Email: {form.email}\n"
        f"Сообщение:\n{form.message}"
    )

    try:
        # Подключаемся к SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()             # шифруем соединение
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        logger.info(f"Сообщение успешно отправлено: {form.dict()}")
        return {"status": "success", "message": "Сообщение отправлено на email!"}

    except Exception as e:
        # Если что-то пошло не так — просто логируем
        logger.error(f"Ошибка при отправке письма: {e}")
        logger.info(f"Попытка отправки: {form.dict()}")
        return {"status": "error", "message": "Не удалось отправить письмо, но данные сохранены."}

