# ⚡ Быстрый старт - Тестирование

## 🚀 Основные команды

```bash
# Активация окружения
source .venv/bin/activate

# Запуск ВСЕХ тестов
pytest

# С подробным выводом
pytest -v

# С покрытием кода
pytest --cov=app

# HTML отчет о покрытии
pytest --cov=app --cov-report=html && firefox htmlcov/index.html
```

## 🎯 Быстрые проверки

```bash
# Только тесты эндпоинтов
pytest tests/test_endpoints.py -v

# Только тесты контактной формы
pytest tests/test_contact_form.py -v

# Только демонстрация заглушки
pytest tests/test_email_stub.py -v

# Конкретный тест
pytest tests/test_endpoints.py::TestHomeEndpoint::test_home_page_returns_200 -v
```

## 🔒 Управление заглушкой email

### В тестах (по умолчанию)
```bash
pytest  # DISABLE_EMAIL=true автоматически
# Результат: ✅ Нет спама на adrolv@rambler.ru
```

### При локальной разработке
```bash
# БЕЗ отправки email (тестирование UI)
DISABLE_EMAIL=true uvicorn app.main:app --reload

# С реальной отправкой
uvicorn app.main:app --reload
```

### В Docker
```bash
# БЕЗ отправки
DISABLE_EMAIL=true docker compose up

# С отправкой (продакшен)
docker compose up
```

## 📊 Текущие результаты

```
✅ Тестов:    61
📊 Покрытие:  98.45%
⏱️  Время:    ~1 секунда
📧 Email:     0 (заглушка активна)
```

## 📁 Что читать

| Файл | Описание |
|------|----------|
| `TESTS_SUMMARY.md` | Краткая сводка |
| `TESTING.md` | Полная документация |
| `EMAIL_STUB.md` | Про заглушку email |
| `tests/README.md` | Детали тестов |

## 🐛 Отладка

```bash
# С выводом print
pytest -s

# Остановка на первой ошибке
pytest -x

# Полный traceback
pytest --tb=long

# С отладчиком
pytest --pdb
```

## ✨ Примеры

### Проверить, что главная страница работает
```bash
pytest tests/test_endpoints.py::TestHomeEndpoint -v
```

### Проверить контактную форму
```bash
pytest tests/test_contact_form.py -v
```

### Проверить заглушку email
```bash
pytest tests/test_email_stub.py -v -s
# Увидишь: [ТЕСТОВЫЙ РЕЖИМ] Email не отправлен
```

## 🎉 Быстрая проверка

Одна команда для проверки всего:

```bash
pytest -v --cov=app --cov-report=term-missing:skip-covered
```

Результат:
- ✅ 61 тест пройден
- 📊 98.45% покрытия
- ⚡ ~1 секунда
- 📧 0 спама

---

**Всё готово! Запускай тесты когда угодно без риска спама! 🚀**
