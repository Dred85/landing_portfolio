"""
Демонстрация работы заглушки email
"""
import pytest
from fastapi import status


class TestEmailStubDemonstration:
    """
    Эти тесты демонстрируют, что заглушка работает:
    - Email НЕ отправляется на реальную почту
    - Форма обрабатывается успешно
    - В логах видно "[ТЕСТОВЫЙ РЕЖИМ]"
    """

    def test_contact_form_with_stub_no_real_email(self, client, valid_contact_data, caplog):
        """POST /contact с заглушкой - реальный email НЕ отправляется"""
        response = client.post("/contact", data=valid_contact_data)
        
        assert response.status_code == status.HTTP_200_OK
        # Проверяем, что в логах есть отметка о тестовом режиме
        assert "[ТЕСТОВЫЙ РЕЖИМ]" in caplog.text
        assert "Email не отправлен" in caplog.text

    def test_api_contact_with_stub_no_real_email(self, client, valid_contact_data, caplog):
        """POST /api/contact с заглушкой - реальный email НЕ отправляется"""
        response = client.post("/api/contact", json=valid_contact_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Успех, но email не отправлен
        assert data["status"] == "success"
        assert "тестовый режим" in data["message"].lower()
        
        # Проверяем логи
        assert "[ТЕСТОВЫЙ РЕЖИМ]" in caplog.text

    def test_multiple_submissions_no_spam(self, client, valid_contact_data, caplog):
        """
        Множественные отправки форм НЕ создают спам на реальной почте.
        Все обрабатываются через заглушку.
        """
        # Отправляем форму 10 раз
        for i in range(10):
            response = client.post("/api/contact", json={
                **valid_contact_data,
                "message": f"Test message #{i}"
            })
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["status"] == "success"
        
        # Проверяем, что все 10 запросов обработаны через заглушку
        assert caplog.text.count("[ТЕСТОВЫЙ РЕЖИМ]") >= 10
        
    def test_stub_logs_form_data(self, client, valid_contact_data, caplog):
        """Заглушка логирует данные формы для отладки"""
        response = client.post("/api/contact", json=valid_contact_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Проверяем, что данные залогированы
        assert valid_contact_data["name"] in caplog.text
        assert valid_contact_data["email"] in caplog.text
        assert valid_contact_data["message"] in caplog.text
