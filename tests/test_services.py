"""
Тесты для сервисов приложения
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from app.services.contact_service import process_contact_form
from app.schemas.contact import ContactForm


class TestContactServiceWithStub:
    """Тесты с заглушкой email (DISABLE_EMAIL=true)"""

    @pytest.mark.asyncio
    async def test_email_disabled_returns_success(self, valid_contact_data):
        """При DISABLE_EMAIL=true email не отправляется, но возвращается success"""
        # DISABLE_EMAIL уже установлен в conftest.py через fixture
        form = ContactForm(**valid_contact_data)
        result = await process_contact_form(form)
        
        assert result["status"] == "success"
        assert "тестовый режим" in result["message"].lower() or "не отправлен" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_email_disabled_no_smtp_called(self, valid_contact_data):
        """При DISABLE_EMAIL=true SMTP не вызывается"""
        with patch('app.services.contact_service.smtplib.SMTP_SSL') as mock_smtp_ssl, \
             patch('app.services.contact_service.smtplib.SMTP') as mock_smtp:
            
            form = ContactForm(**valid_contact_data)
            result = await process_contact_form(form)
            
            # SMTP вообще не должен вызываться
            mock_smtp_ssl.assert_not_called()
            mock_smtp.assert_not_called()
            assert result["status"] == "success"


class TestContactService:
    """Тесты для contact_service"""

    @pytest.mark.asyncio
    @patch('app.services.contact_service.smtplib.SMTP_SSL')
    async def test_process_contact_form_success_ssl(self, mock_smtp, valid_contact_data, monkeypatch):
        """Тест успешной обработки формы через SSL (порт 465)"""
        # Отключаем заглушку для проверки реальной логики
        monkeypatch.setenv("DISABLE_EMAIL", "false")
        
        # Мокаем SMTP сервер
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        with patch('app.services.contact_service.SMTP_PORT', 465):
            form = ContactForm(**valid_contact_data)
            result = await process_contact_form(form)

        assert result["status"] == "success"
        assert "отправлено" in result["message"].lower() or "sent" in result["message"].lower()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_contact_form_success_starttls(self, valid_contact_data, monkeypatch):
        """Тест успешной обработки формы через STARTTLS (порт 587)"""
        # Отключаем заглушку для проверки реальной логики
        monkeypatch.setenv("DISABLE_EMAIL", "false")
        
        # Мокаем SMTP сервер для STARTTLS
        with patch('app.services.contact_service.SMTP_PORT', 587), \
             patch('app.services.contact_service.smtplib.SMTP') as mock_smtp:
            
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            form = ContactForm(**valid_contact_data)
            result = await process_contact_form(form)

            assert result["status"] == "success"
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once()
            mock_server.send_message.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.services.contact_service.smtplib.SMTP_SSL')
    async def test_process_contact_form_smtp_error(self, mock_smtp, valid_contact_data, monkeypatch):
        """Тест обработки ошибки SMTP"""
        # Отключаем заглушку для проверки реальной логики
        monkeypatch.setenv("DISABLE_EMAIL", "false")
        
        # Симулируем ошибку SMTP
        mock_smtp.return_value.__enter__.side_effect = Exception("SMTP Error")

        with patch('app.services.contact_service.SMTP_PORT', 465):
            form = ContactForm(**valid_contact_data)
            result = await process_contact_form(form)

        assert result["status"] == "error"
        assert "ошибка" in result["message"].lower() or "error" in result["message"].lower()

    @pytest.mark.asyncio
    @patch('app.services.contact_service.smtplib.SMTP_SSL')
    async def test_process_contact_form_login_error(self, mock_smtp, valid_contact_data, monkeypatch):
        """Тест обработки ошибки авторизации SMTP"""
        # Отключаем заглушку для проверки реальной логики
        monkeypatch.setenv("DISABLE_EMAIL", "false")
        
        # Мокаем SMTP сервер с ошибкой авторизации
        mock_server = MagicMock()
        mock_server.login.side_effect = Exception("535 5.7.0 Invalid login or password")
        mock_smtp.return_value.__enter__.return_value = mock_server

        with patch('app.services.contact_service.SMTP_PORT', 465):
            form = ContactForm(**valid_contact_data)
            result = await process_contact_form(form)

        assert result["status"] == "error"
        assert "ошибка" in result["message"].lower() or "error" in result["message"].lower()

    @pytest.mark.asyncio
    @patch('app.services.contact_service.smtplib.SMTP_SSL')
    async def test_email_message_format(self, mock_smtp, valid_contact_data, monkeypatch):
        """Тест правильного форматирования email сообщения"""
        # Отключаем заглушку для проверки реальной логики
        monkeypatch.setenv("DISABLE_EMAIL", "false")
        
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        with patch('app.services.contact_service.SMTP_PORT', 465):
            form = ContactForm(**valid_contact_data)
            await process_contact_form(form)

        # Проверяем, что send_message был вызван
        assert mock_server.send_message.called
        
        # Получаем переданное сообщение
        call_args = mock_server.send_message.call_args
        sent_message = call_args[0][0] if call_args[0] else None
        
        if sent_message:
            # Проверяем базовую структуру сообщения
            assert sent_message['Subject']
            assert sent_message['From']
            assert sent_message['To']
            # Проверяем, что в теме есть имя отправителя
            assert valid_contact_data["name"] in sent_message['Subject']

    @pytest.mark.asyncio
    @patch('app.services.contact_service.smtplib.SMTP_SSL')
    async def test_environment_variables_used(self, mock_smtp, valid_contact_data, monkeypatch):
        """Тест использования переменных окружения"""
        # Отключаем заглушку для проверки реальной логики
        monkeypatch.setenv("DISABLE_EMAIL", "false")
        
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        with patch('app.services.contact_service.SMTP_PORT', 465), \
             patch('app.services.contact_service.SMTP_SERVER', 'test.smtp.ru'), \
             patch('app.services.contact_service.SMTP_USER', 'test@test.ru'):
            
            form = ContactForm(**valid_contact_data)
            await process_contact_form(form)

        # Проверяем, что SMTP был вызван с правильными параметрами
        mock_smtp.assert_called_once()
        # Первый аргумент должен быть server, второй - port
        assert mock_smtp.call_args[0][0] == 'test.smtp.ru'
        assert mock_smtp.call_args[0][1] == 465
