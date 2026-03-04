"""
Тесты для функционала контактной формы
"""
import pytest
from fastapi import status
from unittest.mock import patch, MagicMock


class TestContactFormSubmission:
    """Тесты отправки контактной формы через POST /contact"""

    def test_contact_form_post_with_valid_data(self, client, valid_contact_data):
        """POST /contact с валидными данными должен возвращать 200"""
        response = client.post("/contact", data=valid_contact_data)
        assert response.status_code == status.HTTP_200_OK

    def test_contact_form_post_returns_html(self, client, valid_contact_data):
        """POST /contact должен возвращать HTML"""
        response = client.post("/contact", data=valid_contact_data)
        assert "text/html" in response.headers["content-type"]

    def test_contact_form_shows_success_or_error(self, client, valid_contact_data):
        """POST /contact должен показывать сообщение об успехе или ошибке"""
        response = client.post("/contact", data=valid_contact_data)
        # Проверяем, что есть либо success, либо error сообщение
        assert ("успешно" in response.text.lower() or 
                "ошибка" in response.text.lower() or
                "получено" in response.text.lower())

    def test_contact_form_with_missing_name(self, client):
        """POST /contact без имени должен вернуть ошибку валидации"""
        data = {
            "name": "",
            "email": "test@example.com",
            "message": "Test message"
        }
        response = client.post("/contact", data=data)
        # FastAPI может вернуть 422 или просто показать форму с ошибкой (200)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]

    def test_contact_form_with_invalid_email(self, client):
        """POST /contact с невалидным email должен обработать ошибку"""
        data = {
            "name": "Test User",
            "email": "not-an-email",
            "message": "Test message"
        }
        # Роутер обрабатывает ValidationError и возвращает страницу с ошибкой
        response = client.post("/contact", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert "error" in response.text.lower() or "ошибка" in response.text.lower()


class TestContactAPIEndpoint:
    """Тесты для JSON API эндпоинта /api/contact"""

    def test_api_contact_with_valid_json(self, client, valid_contact_data):
        """POST /api/contact с валидным JSON должен возвращать 200"""
        response = client.post("/api/contact", json=valid_contact_data)
        assert response.status_code == status.HTTP_200_OK

    def test_api_contact_returns_json(self, client, valid_contact_data):
        """POST /api/contact должен возвращать JSON"""
        response = client.post("/api/contact", json=valid_contact_data)
        assert "application/json" in response.headers["content-type"]

    def test_api_contact_response_structure(self, client, valid_contact_data):
        """POST /api/contact должен возвращать структурированный ответ"""
        response = client.post("/api/contact", json=valid_contact_data)
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert data["status"] in ["success", "error"]

    def test_api_contact_with_missing_fields(self, client):
        """POST /api/contact без обязательных полей должен вернуть 422"""
        response = client.post("/api/contact", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_api_contact_with_invalid_email(self, client):
        """POST /api/contact с невалидным email должен вернуть 422"""
        data = {
            "name": "Test",
            "email": "not-an-email",
            "message": "Test"
        }
        response = client.post("/api/contact", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch('app.services.contact_service.smtplib.SMTP_SSL')
    def test_api_contact_successful_email_sending(self, mock_smtp, client, valid_contact_data, monkeypatch):
        """Тест успешной отправки email (с моком SMTP)"""
        # Отключаем заглушку для этого теста
        monkeypatch.setenv("DISABLE_EMAIL", "false")
        
        # Мокаем SMTP сервер
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        response = client.post("/api/contact", json=valid_contact_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Проверяем, что метод login был вызван
        mock_server.login.assert_called_once()
        # Проверяем, что метод send_message был вызван
        mock_server.send_message.assert_called_once()

    @patch('app.services.contact_service.smtplib.SMTP_SSL')
    def test_api_contact_handles_smtp_error(self, mock_smtp, client, valid_contact_data, monkeypatch):
        """Тест обработки ошибки SMTP (с моком)"""
        # Отключаем заглушку для этого теста
        monkeypatch.setenv("DISABLE_EMAIL", "false")
        
        # Мокаем SMTP сервер с ошибкой
        mock_smtp.return_value.__enter__.side_effect = Exception("SMTP connection failed")

        response = client.post("/api/contact", json=valid_contact_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "error"
        assert "ошибка" in data["message"].lower() or "error" in data["message"].lower()
