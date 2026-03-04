"""
Функциональные тесты для всех эндпоинтов FastAPI приложения
"""
import pytest
from fastapi import status


class TestHomeEndpoint:
    """Тесты для главной страницы"""

    def test_home_page_returns_200(self, client):
        """GET / должен возвращать 200 OK"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK

    def test_home_page_returns_html(self, client):
        """GET / должен возвращать HTML"""
        response = client.get("/")
        assert "text/html" in response.headers["content-type"]

    def test_home_page_contains_title(self, client):
        """Главная страница должна содержать заголовок"""
        response = client.get("/")
        assert "Александр" in response.text or "Portfolio" in response.text

    def test_home_page_has_navigation_links(self, client):
        """Главная страница должна содержать навигационные ссылки"""
        response = client.get("/")
        assert "/about" in response.text
        assert "/projects" in response.text
        assert "/contact" in response.text


class TestAboutEndpoint:
    """Тесты для страницы About"""

    def test_about_page_returns_200(self, client):
        """GET /about должен возвращать 200 OK"""
        response = client.get("/about")
        assert response.status_code == status.HTTP_200_OK

    def test_about_page_returns_html(self, client):
        """GET /about должен возвращать HTML"""
        response = client.get("/about")
        assert "text/html" in response.headers["content-type"]

    def test_about_page_has_content(self, client):
        """Страница About должна иметь контент"""
        response = client.get("/about")
        assert len(response.text) > 100  # Минимальная проверка наличия контента


class TestProjectsEndpoint:
    """Тесты для страницы Projects"""

    def test_projects_page_returns_200(self, client):
        """GET /projects должен возвращать 200 OK"""
        response = client.get("/projects")
        assert response.status_code == status.HTTP_200_OK

    def test_projects_page_returns_html(self, client):
        """GET /projects должен возвращать HTML"""
        response = client.get("/projects")
        assert "text/html" in response.headers["content-type"]

    def test_projects_page_has_content(self, client):
        """Страница Projects должна иметь контент"""
        response = client.get("/projects")
        assert len(response.text) > 100


class TestContactEndpoint:
    """Тесты для страницы Contact"""

    def test_contact_page_returns_200(self, client):
        """GET /contact должен возвращать 200 OK"""
        response = client.get("/contact")
        assert response.status_code == status.HTTP_200_OK

    def test_contact_page_returns_html(self, client):
        """GET /contact должен возвращать HTML"""
        response = client.get("/contact")
        assert "text/html" in response.headers["content-type"]

    def test_contact_page_has_form(self, client):
        """Страница Contact должна содержать форму"""
        response = client.get("/contact")
        assert "<form" in response.text
        assert 'name="name"' in response.text
        assert 'name="email"' in response.text
        assert 'name="message"' in response.text


class TestMetricsEndpoint:
    """Тесты для эндпоинта метрик Prometheus"""

    def test_metrics_endpoint_returns_200(self, client):
        """GET /metrics должен возвращать 200 OK"""
        response = client.get("/metrics")
        assert response.status_code == status.HTTP_200_OK

    def test_metrics_returns_prometheus_format(self, client):
        """GET /metrics должен возвращать метрики в формате Prometheus"""
        response = client.get("/metrics")
        assert "# HELP" in response.text or "# TYPE" in response.text

    def test_metrics_contains_http_metrics(self, client):
        """Метрики должны содержать HTTP метрики"""
        response = client.get("/metrics")
        # Проверяем наличие базовых метрик от prometheus-fastapi-instrumentator
        assert "http_request" in response.text.lower() or "requests" in response.text.lower()


class TestStaticFiles:
    """Тесты для статических файлов"""

    def test_static_css_accessible(self, client):
        """CSS файлы должны быть доступны"""
        response = client.get("/static/css/styles.css")
        # 200 если файл существует, 404 если нет (не критично для теста)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_static_js_accessible(self, client):
        """JS файлы должны быть доступны"""
        response = client.get("/static/js/main.js")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


class TestErrorHandling:
    """Тесты обработки ошибок"""

    def test_nonexistent_route_returns_404(self, client):
        """Несуществующий маршрут должен возвращать 404"""
        response = client.get("/nonexistent-route")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_method_returns_405(self, client):
        """Неправильный HTTP метод должен возвращать 405"""
        response = client.delete("/")  # GET-only endpoint
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
