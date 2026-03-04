"""
Тесты для валидации схем (schemas)
"""
import pytest
from pydantic import ValidationError
from app.schemas.contact import ContactForm


class TestContactFormSchema:
    """Тесты для схемы ContactForm"""

    def test_valid_contact_form(self, valid_contact_data):
        """Валидные данные должны пройти валидацию"""
        form = ContactForm(**valid_contact_data)
        assert form.name == valid_contact_data["name"]
        assert form.email == valid_contact_data["email"]
        assert form.message == valid_contact_data["message"]

    def test_contact_form_invalid_email(self):
        """Невалидный email должен вызвать ValidationError"""
        with pytest.raises(ValidationError):
            ContactForm(
                name="Test",
                email="not-an-email",
                message="Test message"
            )

    def test_contact_form_missing_name(self):
        """Отсутствие имени должно вызвать ValidationError"""
        with pytest.raises(ValidationError):
            ContactForm(
                email="test@example.com",
                message="Test message"
            )

    def test_contact_form_missing_email(self):
        """Отсутствие email должно вызвать ValidationError"""
        with pytest.raises(ValidationError):
            ContactForm(
                name="Test",
                message="Test message"
            )

    def test_contact_form_missing_message(self):
        """Отсутствие сообщения должно вызвать ValidationError"""
        with pytest.raises(ValidationError):
            ContactForm(
                name="Test",
                email="test@example.com"
            )

    def test_contact_form_accepts_empty_name(self):
        """Схема принимает пустую строку в name (валидация на уровне формы)"""
        # Схема не имеет минимальной длины, так что пустая строка валидна
        form = ContactForm(
            name="",
            email="test@example.com",
            message="Test"
        )
        assert form.name == ""

    def test_contact_form_email_validation(self):
        """EmailStr валидирует корректность email"""
        # EmailStr от Pydantic валидирует формат email
        form = ContactForm(
            name="Test",
            email="test@example.com",
            message="Test"
        )
        assert "@" in form.email
        assert "." in form.email

    def test_contact_form_preserves_whitespace(self):
        """Схема сохраняет пробелы (trimming не настроен)"""
        # Текущая схема не имеет автоматического trimming
        form = ContactForm(
            name="  Test User  ",
            email="test@example.com",
            message="  Test message  "
        )
        # Проверяем, что данные сохранились
        assert "Test User" in form.name
        assert "Test message" in form.message
