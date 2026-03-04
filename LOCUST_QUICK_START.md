# ⚡ Locust - Быстрый старт

## 🔒 ШАГ 1: Включи заглушку email!

**ОБЯЗАТЕЛЬНО перед запуском POST тестов!**

```bash
# Добавь в .env файл:
echo "DISABLE_EMAIL=true" >> .env

# Или открой .env и добавь:
# DISABLE_EMAIL=true
```

Иначе придёт **много спама** на `adrolv@rambler.ru`! 📧🚫

## 🚀 ШАГ 2: Запусти тесты

### Вариант A: Полный тест (5 минут)

```bash
docker compose up --build
```

**Откроется:**
- 🐝 Locust UI: http://localhost:8089
- 📊 Grafana: http://localhost:3000
- 📈 Prometheus: http://localhost:9090

### Вариант B: Быстрый тест (3 минуты)

```bash
docker compose -f docker-compose.performance.yml up --build
```

Автоматически запустится и завершится через 3 минуты.

## 📊 ШАГ 3: Смотри результаты

### В Locust UI (http://localhost:8089)

```
Type     Name              # reqs  # fails   Avg    Median  req/s
------------------------------------------------------------------
GET      /                 5000    0(0%)     45ms   42      167.0
POST     /contact          500     0(0%)     142ms  135     16.7
------------------------------------------------------------------

✅ 0% failures = все проверки пройдены!
```

### В Grafana (http://localhost:3000)

Логин: `admin` / Пароль: `admin`

Метрики:
- `locust_users` - количество виртуальных пользователей
- `http_request_duration_seconds` - время ответа

## 🎯 Что проверяется

### GET эндпоинты
- ✅ Статус 200
- ✅ Время ответа < **500ms**
- ✅ HTML контент
- ✅ Размер контента

### POST эндпоинты
- ✅ Статус 200
- ✅ Время ответа < **1000ms**
- ✅ Корректный ответ (HTML или JSON)
- ✅ Структура данных

### Метрики
- ✅ Статус 200
- ✅ Время ответа < **200ms**
- ✅ Формат Prometheus

## 🔥 Use Cases

| UC | Эндпоинт | SLA | Описание |
|----|----------|-----|----------|
| UC01 | `GET /` | 500ms | Главная |
| UC02 | `GET /contact` | 500ms | Форма контактов |
| UC03 | `GET /about` | 500ms | О нас |
| UC04 | `GET /projects` | 500ms | Проекты |
| UC05 | `POST /contact` | 1000ms | Отправка формы |
| UC05_API | `POST /api/contact` | 1000ms | JSON API |
| UC06 | `GET /metrics` | 200ms | Метрики |

## 🛑 Остановка тестов

```bash
# Остановить Docker Compose
docker compose down

# Или Ctrl+C
```

## 📝 Лог файлы

```bash
# Логи приложения
docker compose logs web -f

# Логи Locust
docker compose logs locust -f

# Все логи
docker compose logs -f
```

## ✅ Чеклист перед запуском

- [ ] Добавил `DISABLE_EMAIL=true` в `.env`
- [ ] Запустил `docker compose up --build`
- [ ] Открыл Locust UI (http://localhost:8089)
- [ ] Жду результатов (5 минут)
- [ ] Проверяю failures (должно быть 0%)

## 🎉 Готово!

После завершения теста:
1. Проверь **0% failures** в Locust UI
2. Проверь **среднее время ответа** < SLA
3. Проверь **отсутствие спама** на почте
4. Сохрани результаты из Locust UI

---

**🔥 Запускай без опасений - спама НЕ будет! 🔥**

```bash
docker compose up --build
```
