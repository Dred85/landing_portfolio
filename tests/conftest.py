import pytest
import os
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Автоматически устанавливает переменные окружения для тестового режима.
    Включает заглушку email, чтобы не отправлять реальные письма.
    """
    # Сохраняем оригинальное значение
    original_disable_email = os.environ.get("DISABLE_EMAIL")
    
    # Включаем тестовый режим (заглушка email)
    os.environ["DISABLE_EMAIL"] = "true"
    
    yield
    
    # Восстанавливаем оригинальное значение
    if original_disable_email is not None:
        os.environ["DISABLE_EMAIL"] = original_disable_email
    else:
        os.environ.pop("DISABLE_EMAIL", None)


@pytest.fixture
def client():
    """
    Фикстура для TestClient FastAPI приложения.
    Используется для тестирования всех эндпоинтов.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def valid_contact_data():
    """Валидные данные для формы контакта"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "message": "Test message from pytest"
    }


@pytest.fixture
def invalid_contact_data():
    """Невалидные данные для формы контакта"""
    return {
        "name": "",
        "email": "invalid-email",
        "message": ""
    }
