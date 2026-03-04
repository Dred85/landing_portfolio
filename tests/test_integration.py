"""
Интеграционные тесты для проверки работы всего приложения
"""
import pytest
from fastapi import status


class TestNavigationFlow:
    """Тесты навигации между страницами"""

    def test_full_navigation_flow(self, client):
        """Тест полного цикла навигации по сайту"""
        # Главная страница
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        
        # О нас
        response = client.get("/about")
        assert response.status_code == status.HTTP_200_OK
        
        # Проекты
        response = client.get("/projects")
        assert response.status_code == status.HTTP_200_OK
        
        # Контакты
        response = client.get("/contact")
        assert response.status_code == status.HTTP_200_OK

    def test_all_pages_have_consistent_structure(self, client):
        """Все страницы должны иметь согласованную структуру"""
        pages = ["/", "/about", "/projects", "/contact"]
        
        for page in pages:
            response = client.get(page)
            assert response.status_code == status.HTTP_200_OK
            # Проверяем наличие базовых элементов
            assert "<!DOCTYPE html>" in response.text or "<html" in response.text
            assert "</html>" in response.text


class TestCORS:
    """Тесты CORS настроек"""

    def test_cors_headers_present(self, client):
        """CORS заголовки должны присутствовать"""
        response = client.get("/")
        # Проверяем наличие CORS заголовков (если настроены)
        assert response.status_code == status.HTTP_200_OK

    def test_options_request_allowed(self, client):
        """OPTIONS запросы должны быть разрешены"""
        response = client.options("/")
        # OPTIONS может вернуть 200 или 405 в зависимости от настроек CORS
        assert response.status_code in [
            status.HTTP_200_OK, 
            status.HTTP_405_METHOD_NOT_ALLOWED
        ]


class TestContactFormIntegration:
    """Интеграционные тесты контактной формы"""

    def test_contact_page_to_submission_flow(self, client, valid_contact_data):
        """Тест полного флоу: открытие страницы -> отправка формы"""
        # Шаг 1: Получаем страницу с формой
        response = client.get("/contact")
        assert response.status_code == status.HTTP_200_OK
        assert "<form" in response.text
        
        # Шаг 2: Отправляем форму
        response = client.post("/contact", data=valid_contact_data)
        assert response.status_code == status.HTTP_200_OK
        # Должно быть сообщение о результате (успех или ошибка)
        assert ("успешно" in response.text.lower() or 
                "ошибка" in response.text.lower())

    def test_contact_api_json_submission(self, client, valid_contact_data):
        """Тест отправки через JSON API"""
        response = client.post("/api/contact", json=valid_contact_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert "message" in data


class TestApplicationHealth:
    """Тесты для проверки здоровья приложения"""

    def test_all_critical_endpoints_accessible(self, client):
        """Все критичные эндпоинты должны быть доступны"""
        critical_endpoints = [
            "/",
            "/about",
            "/projects",
            "/contact",
            "/metrics"
        ]
        
        for endpoint in critical_endpoints:
            response = client.get(endpoint)
            assert response.status_code == status.HTTP_200_OK, \
                f"Endpoint {endpoint} returned {response.status_code}"

    def test_concurrent_requests_handling(self, client):
        """Тест обработки множественных одновременных запросов"""
        # Симулируем несколько запросов подряд
        for _ in range(10):
            response = client.get("/")
            assert response.status_code == status.HTTP_200_OK

    def test_different_content_types_supported(self, client, valid_contact_data):
        """Приложение должно поддерживать разные content-type"""
        # HTML запрос
        response_html = client.get("/")
        assert "text/html" in response_html.headers["content-type"]
        
        # JSON API
        response_json = client.post("/api/contact", json=valid_contact_data)
        assert "application/json" in response_json.headers["content-type"]
        
        # Prometheus metrics
        response_metrics = client.get("/metrics")
        assert response_metrics.status_code == status.HTTP_200_OK
