# Тесты для FastAPI Portfolio

## Структура тестов

```
tests/
├── __init__.py              # Инициализация пакета тестов
├── conftest.py              # Общие фикстуры pytest
├── test_endpoints.py        # Тесты всех эндпоинтов приложения
├── test_contact_form.py     # Тесты контактной формы
├── test_schemas.py          # Тесты валидации схем Pydantic
└── test_integration.py      # Интеграционные тесты
```

## Покрытие тестами

### 1. test_endpoints.py
- **TestHomeEndpoint**: тесты главной страницы `/`
  - Проверка статуса 200
  - Проверка возврата HTML
  - Проверка содержимого заголовка
  - Проверка навигационных ссылок

- **TestAboutEndpoint**: тесты страницы `/about`
  - Проверка статуса 200
  - Проверка возврата HTML
  - Проверка наличия контента

- **TestProjectsEndpoint**: тесты страницы `/projects`
  - Проверка статуса 200
  - Проверка возврата HTML
  - Проверка наличия контента

- **TestContactEndpoint**: тесты страницы `/contact`
  - Проверка статуса 200
  - Проверка возврата HTML
  - Проверка наличия формы

- **TestMetricsEndpoint**: тесты эндпоинта `/metrics`
  - Проверка статуса 200
  - Проверка формата Prometheus
  - Проверка наличия HTTP метрик

- **TestStaticFiles**: тесты статических файлов
  - Доступность CSS
  - Доступность JS

- **TestErrorHandling**: тесты обработки ошибок
  - 404 для несуществующих маршрутов
  - 405 для неправильных HTTP методов

### 2. test_contact_form.py
- **TestContactFormSubmission**: тесты POST /contact
  - Отправка валидных данных
  - Проверка возврата HTML
  - Проверка отображения сообщений
  - Валидация отсутствия имени
  - Валидация невалидного email

- **TestContactAPIEndpoint**: тесты POST /api/contact
  - Отправка валидного JSON
  - Проверка возврата JSON
  - Проверка структуры ответа
  - Валидация отсутствующих полей
  - Валидация невалидного email
  - Мок-тест успешной отправки email
  - Мок-тест обработки ошибки SMTP

### 3. test_schemas.py
- **TestContactFormSchema**: тесты схемы ContactForm
  - Валидация корректных данных
  - Валидация невалидного email
  - Валидация отсутствующих полей (name, email, message)
  - Валидация пустых строк
  - Нормализация email
  - Удаление пробелов (trimming)

### 4. test_integration.py
- **TestNavigationFlow**: тесты навигации
  - Полный цикл навигации по сайту
  - Согласованность структуры страниц

- **TestCORS**: тесты CORS
  - Проверка CORS заголовков
  - OPTIONS запросы

- **TestContactFormIntegration**: интеграционные тесты формы
  - Полный флоу: страница → отправка
  - JSON API отправка

- **TestApplicationHealth**: тесты здоровья приложения
  - Доступность критичных эндпоинтов
  - Обработка множественных запросов
  - Поддержка разных content-type

## Запуск тестов

### Локально (с активированным виртуальным окружением)

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск конкретного файла
pytest tests/test_endpoints.py

# Запуск конкретного класса
pytest tests/test_endpoints.py::TestHomeEndpoint

# Запуск конкретного теста
pytest tests/test_endpoints.py::TestHomeEndpoint::test_home_page_returns_200

# Запуск с покрытием кода
pytest --cov=app --cov-report=html

# Запуск только интеграционных тестов
pytest -m integration

# Запуск только юнит-тестов
pytest -m unit
```

### В Docker контейнере

```bash
# Запуск тестов внутри web контейнера
docker compose exec web pytest

# С подробным выводом
docker compose exec web pytest -v

# С покрытием
docker compose exec web pytest --cov=app
```

## Добавление новых тестов

1. Создайте новый файл `test_*.py` в директории `tests/`
2. Импортируйте необходимые фикстуры из `conftest.py`
3. Используйте классы для группировки связанных тестов
4. Следуйте паттерну Arrange-Act-Assert

### Пример нового теста:

```python
from fastapi import status

class TestNewFeature:
    """Тесты для новой функции"""
    
    def test_new_endpoint(self, client):
        """Описание теста"""
        # Arrange
        data = {"key": "value"}
        
        # Act
        response = client.post("/new-endpoint", json=data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["result"] == "expected"
```

## Маркеры (Markers)

- `@pytest.mark.integration` - интеграционные тесты
- `@pytest.mark.unit` - юнит-тесты
- `@pytest.mark.slow` - медленные тесты

## Фикстуры

### client
Тестовый клиент FastAPI для выполнения HTTP запросов.

```python
def test_example(client):
    response = client.get("/")
    assert response.status_code == 200
```

### valid_contact_data
Валидные данные для тестирования контактной формы.

```python
def test_example(client, valid_contact_data):
    response = client.post("/contact", data=valid_contact_data)
    assert response.status_code == 200
```

### invalid_contact_data
Невалидные данные для тестирования валидации.

```python
def test_example(client, invalid_contact_data):
    response = client.post("/contact", data=invalid_contact_data)
    # Проверка обработки ошибок
```

## CI/CD Integration

Добавьте в ваш CI/CD пайплайн:

```yaml
test:
  script:
    - pip install -r requirements.txt
    - pytest --cov=app --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
```

## Отладка тестов

```bash
# Запуск с выводом print statements
pytest -s

# Запуск с полным traceback
pytest --tb=long

# Запуск с pdb отладчиком при ошибке
pytest --pdb

# Запуск конкретного теста с подробным выводом
pytest tests/test_contact_form.py::TestContactFormSubmission::test_contact_form_post_with_valid_data -vv -s
```
