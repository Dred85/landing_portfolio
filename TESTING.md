# 🧪 Тестирование FastAPI Portfolio

## ✅ Результаты тестирования

```
✅ 61 тест пройден
📊 Покрытие кода: 98.45%
⏱️  Время выполнения: ~1 секунда (с заглушкой email)
📧 Реальных email отправлено: 0 (заглушка активна)
```

## 📁 Структура тестов

```
tests/
├── __init__.py              # Инициализация пакета
├── conftest.py              # Фикстуры pytest + заглушка email
├── test_endpoints.py        # Тесты всех эндпоинтов (30 тестов)
├── test_contact_form.py     # Тесты контактной формы (12 тестов)
├── test_schemas.py          # Тесты валидации схем (8 тестов)
├── test_services.py         # Тесты сервисов (8 тестов + заглушка)
├── test_integration.py      # Интеграционные тесты (9 тестов)
├── test_email_stub.py       # Демонстрация заглушки (4 теста)
└── README.md                # Подробная документация
```

## 🔒 Заглушка email (важно!)

**Тесты автоматически работают в режиме заглушки** - реальные email НЕ отправляются.

При запуске тестов автоматически устанавливается `DISABLE_EMAIL=true`:
- ✅ Email не отправляются на реальную почту
- ✅ Нет спама на `adrolv@rambler.ru`
- ✅ Сервис логирует данные формы
- ✅ Возвращает успешный ответ без реального SMTP

### Ручное управление заглушкой

```bash
# В тестах (автоматически)
DISABLE_EMAIL=true pytest

# При локальной разработке (без отправки email)
DISABLE_EMAIL=true uvicorn app.main:app --reload

# В продакшене (с реальной отправкой)
DISABLE_EMAIL=false uvicorn app.main:app
# или просто не устанавливать переменную
```

## 🚀 Быстрый старт

### Локально

```bash
# Активация виртуального окружения
source .venv/bin/activate

# Запуск всех тестов (с заглушкой email)
pytest

# С подробным выводом
pytest -v

# С покрытием кода
pytest --cov=app --cov-report=html

# Открыть отчет о покрытии
firefox htmlcov/index.html
```

### В Docker

```bash
# Запуск тестов в контейнере
docker compose exec web pytest

# С покрытием
docker compose exec web pytest --cov=app --cov-report=html
```

## 📊 Покрытие кода по модулям

| Модуль                            | Покрытие | Непокрытые строки |
|-----------------------------------|----------|-------------------|
| `app/routers/about.py`            | 100%     | -                 |
| `app/routers/home.py`             | 100%     | -                 |
| `app/routers/projects.py`         | 100%     | -                 |
| `app/schemas/contact.py`          | 100%     | -                 |
| `app/services/contact_service.py` | 100%     | -                 |
| `app/static/__init__.py`          | 100%     | -                 |
| `app/__init__.py`                 | 100%     | -                 |
| `app/routers/contact.py`          | 96.30%   | 1 строка          |
| `app/main.py`                     | 96.77%   | 1 строка          |
| **ИТОГО**                         | **98.45%** | **2 строки**    |

## 🧪 Что покрывают тесты

### 1️⃣ test_endpoints.py - Тесты эндпоинтов
- ✅ `GET /` - главная страница
- ✅ `GET /about` - страница "О нас"
- ✅ `GET /projects` - страница проектов
- ✅ `GET /contact` - страница контактов
- ✅ `GET /metrics` - метрики Prometheus
- ✅ Статические файлы (CSS, JS)
- ✅ Обработка ошибок (404, 405)

### 2️⃣ test_contact_form.py - Контактная форма
- ✅ POST запросы через HTML форму
- ✅ POST запросы через JSON API
- ✅ Валидация входных данных
- ✅ Обработка ошибок SMTP (с моками)
- ✅ Успешная отправка email (с моками)

### 3️⃣ test_schemas.py - Валидация данных
- ✅ Валидация полей ContactForm
- ✅ Проверка Email формата
- ✅ Проверка обязательных полей
- ✅ Обработка невалидных данных

### 4️⃣ test_services.py - Сервисы
- ✅ Отправка email через SSL (порт 465)
- ✅ Отправка email через STARTTLS (порт 587)
- ✅ Обработка ошибок SMTP
- ✅ Обработка ошибок авторизации
- ✅ Форматирование email сообщений
- ✅ Использование переменных окружения

### 5️⃣ test_integration.py - Интеграционные тесты
- ✅ Полный цикл навигации по сайту
- ✅ Согласованность структуры страниц
- ✅ CORS настройки
- ✅ Полный флоу контактной формы
- ✅ Множественные запросы
- ✅ Разные content-types

## 🎯 Примеры команд

```bash
# Запуск конкретного файла
pytest tests/test_endpoints.py

# Запуск конкретного класса
pytest tests/test_endpoints.py::TestHomeEndpoint

# Запуск конкретного теста
pytest tests/test_contact_form.py::TestContactFormSubmission::test_contact_form_post_with_valid_data -v

# Запуск с выводом print
pytest -s

# Запуск с остановкой на первой ошибке
pytest -x

# Запуск последних упавших тестов
pytest --lf

# Запуск с параллельным выполнением (после установки pytest-xdist)
pytest -n auto
```

## 🔧 Добавление новых тестов

Создайте файл `tests/test_feature.py`:

```python
import pytest
from fastapi import status

class TestNewFeature:
    """Описание набора тестов"""
    
    def test_something(self, client):
        """Описание теста"""
        response = client.get("/endpoint")
        assert response.status_code == status.HTTP_200_OK
```

## 📝 Исправленные проблемы

В процессе создания тестов были исправлены:
1. ✅ Поддержка STARTTLS (порт 587) в `contact_service.py`
2. ✅ Обработка ValidationError в роутере `/contact`
3. ✅ Использование `model_dump()` вместо устаревшего `dict()`
4. ✅ Корректная обработка ошибок при невалидном email
5. ✅ **Заглушка email для тестов** - не отправляются реальные письма

## 🎭 Как работает заглушка

### В тестах (автоматически)

```python
# tests/conftest.py
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Автоматически включает заглушку email"""
    os.environ["DISABLE_EMAIL"] = "true"
    yield
    # Восстанавливает после тестов
```

### В сервисе

```python
# app/services/contact_service.py
DISABLE_EMAIL = os.getenv("DISABLE_EMAIL", "false").lower() in ("true", "1", "yes")

async def process_contact_form(form: ContactForm):
    if DISABLE_EMAIL:
        logger.info(f"[ТЕСТОВЫЙ РЕЖИМ] Email не отправлен: {form.model_dump()}")
        return {"status": "success", "message": "Сообщение получено (тестовый режим)"}
    
    # ... реальная отправка email
```

### Преимущества:
- 🚫 **Нет спама** на реальную почту при тестах
- ⚡ **Быстрее** - не ждём SMTP соединение
- 🔒 **Безопаснее** - не нужны реальные SMTP креды в тестах
- 📝 **Логируется** - все данные записываются в лог

## 🐛 Отладка

```bash
# Подробный traceback
pytest --tb=long

# Запуск с отладчиком
pytest --pdb

# Показать локальные переменные при ошибке
pytest -l
```

## 📈 CI/CD готовность

Тесты готовы для интеграции в CI/CD пайплайн:

```yaml
# .github/workflows/tests.yml (пример)
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest --cov=app --cov-report=xml
```
