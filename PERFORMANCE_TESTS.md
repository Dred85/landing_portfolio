# 🚀 Тесты производительности (Locust)

## ✅ Что добавлено

### 🎯 Проверки производительности в каждом UC

Все Use Cases теперь включают проверки:
- ✅ **Статус код = 200**
- ✅ **Время ответа** (SLA)
- ✅ **Размер контента**
- ✅ **Content-Type**
- ✅ **Структура ответа**

### 📋 Обновлённые Use Cases

| UC | Эндпоинт | Метод | SLA | Проверки |
|----|----------|-------|-----|----------|
| **UC01** | `/` | GET | < 500ms | Статус, время, контент > 1KB, HTML |
| **UC02** | `/contact` | GET | < 500ms | Статус, время, наличие формы, HTML |
| **UC03** | `/about` | GET | < 500ms | Статус, время, контент > 500B, HTML |
| **UC04** | `/projects` | GET | < 500ms | Статус, время, контент > 500B, HTML |
| **UC05** | `/contact` | POST | < 1000ms | Статус, время, сообщение результата |
| **UC05_API** | `/api/contact` | POST | < 1000ms | Статус, время, JSON структура |
| **UC06** | `/metrics` | GET | < 200ms | Статус, время, формат Prometheus |

## 🔒 Важно: Заглушка email!

Для **избежания спама** при POST тестах добавь в `.env`:

```env
DISABLE_EMAIL=true
```

Тогда:
- ✅ POST запросы будут обрабатываться
- ✅ Производительность будет тестироваться
- 🚫 Email НЕ будут отправляться на `adrolv@rambler.ru`
- 📝 Всё логируется: `[ТЕСТОВЫЙ РЕЖИМ]`

## 🚀 Запуск тестов производительности

### Вариант 1: Основной loadshape (стабильность)

```bash
# Добавь в .env:
# DISABLE_EMAIL=true

# Запуск через Docker Compose
docker compose up --build

# Открой в браузере:
# - Locust UI: http://localhost:8089
# - Grafana: http://localhost:3000
# - Prometheus: http://localhost:9090
```

**Этапы теста:**
1. 20s - 20 юзеров на `/` (прогрев)
2. 40s - 40 юзеров на `/about`
3. 60s - 60 юзеров на `/projects`
4. 80s - 60 юзеров на `/contact` (GET)
5. 100s - 40 юзеров на `/contact` (POST) 🔥
6. 120s - 50 юзеров на `/api/contact` (JSON) 🔥
7. 140s - 30 юзеров на `/metrics`
8. 300s - 80 юзеров (все GET + метрики)

### Вариант 2: Быстрый тест производительности (3 минуты)

```bash
# Использует loadshape_performance.py
docker compose -f docker-compose.performance.yml up --build

# Автоматически завершится через 3 минуты
```

**Этапы быстрого теста:**
1. 30s - 10 юзеров (GET прогрев)
2. 60s - 30 юзеров (GET нагрузка)
3. 90s - 20 юзеров (POST форма) 🔥
4. 120s - 25 юзеров (POST API) 🔥
5. 150s - 15 юзеров (метрики)
6. 180s - 50 юзеров (финал GET + метрики)

### Вариант 3: Локальный запуск

```bash
# С заглушкой email
DISABLE_EMAIL=true uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Locust
cd locust
locust -f loadshape_performance.py --host=http://localhost:8000 --headless --run-time 3m
```

## 📊 Мониторинг результатов

### В Locust UI (http://localhost:8089)

Смотри:
- **Requests/s** - запросов в секунду
- **Failures** - количество проваленных проверок
- **Response time (ms)** - время ответа
  - 50th percentile - медиана
  - 95th percentile - SLA граница
  - 99th percentile - worst case

### В Grafana (http://localhost:3000)

Дашборды:
- **Locust Users** - количество виртуальных пользователей
- **HTTP Request Rate** - частота запросов
- **Response Time** - время ответа
- **Error Rate** - процент ошибок

## ✅ Критерии успешности

### GET эндпоинты (/, /about, /projects, /contact)
- ✅ Статус код: **200**
- ✅ P95 время ответа: **< 500ms**
- ✅ P99 время ответа: **< 800ms**
- ✅ Error rate: **< 1%**
- ✅ Throughput: **> 100 req/s** при 50 пользователях

### POST эндпоинты (/contact, /api/contact)
- ✅ Статус код: **200**
- ✅ P95 время ответа: **< 1000ms**
- ✅ P99 время ответа: **< 1500ms**
- ✅ Error rate: **< 1%**
- ✅ Throughput: **> 50 req/s** при 25 пользователях

### Метрики (/metrics)
- ✅ Статус код: **200**
- ✅ P95 время ответа: **< 200ms**
- ✅ P99 время ответа: **< 300ms**
- ✅ Error rate: **0%**
- ✅ Throughput: **> 200 req/s**

## 🔍 Примеры проверок в коде

### UC01 - Главная страница

```python
def open_index(user):
    with user.client.get("/", catch_response=True) as response:
        if response.status_code != 200:
            response.failure(f"Статус {response.status_code}")
        elif response.elapsed.total_seconds() > 0.5:
            response.failure(f"Медленно: {response.elapsed.total_seconds():.3f}s")
        else:
            response.success()
```

### UC05 - POST контактная форма

```python
def submit_contact_form(user):
    form_data = {
        "name": "Locust Test User",
        "email": "locust@test.com",
        "message": "Performance test"
    }
    
    with user.client.post("/contact", data=form_data, catch_response=True) as response:
        if response.status_code != 200:
            response.failure(f"Статус {response.status_code}")
        elif response.elapsed.total_seconds() > 1.0:
            response.failure(f"Медленно: {response.elapsed.total_seconds():.3f}s")
        else:
            response.success()
```

## 📈 Анализ результатов

### Успешный тест выглядит так:

```
Type     Name                      # reqs  # fails   Avg   Min   Max    Median  req/s
-----------------------------------------------------------------------------------------
GET      /                         5000    0         45    23    234    42      167.0
GET      /about                    3000    0         52    28    198    48      100.0
GET      /contact                  2500    0         58    31    215    54      83.5
POST     /contact                  500     0         142   87    456    135     16.7
POST     /api/contact              750     0         128   78    398    122     25.0
GET      /metrics                  1000    0         12    8     45     11      33.3
-----------------------------------------------------------------------------------------
Total                              12750   0         67    8     456    52      425.5

✅ Все проверки пройдены!
✅ Нет спама на почту (DISABLE_EMAIL=true)
✅ SLA соблюдены
```

### Проваленный тест (пример):

```
GET      /contact                  2500    45(1.8%)  1234  31   5000   987     83.5
                                         ^^^ failures

Failures:
  • 23 requests: "Слишком медленный ответ: 1.234s (ожидалось < 0.5s)"
  • 22 requests: "Ожидался статус 200, получен 500"
```

## 🐛 Отладка проблем производительности

### Медленные ответы

```bash
# Проверь логи приложения
docker compose logs web -f

# Проверь метрики в Prometheus
# Query: histogram_quantile(0.95, http_request_duration_seconds_bucket)
```

### Ошибки в ответах

```bash
# Логи Locust
docker compose logs locust -f

# Проверь статус код и детали ошибок в Locust UI
# http://localhost:8089/failures
```

## 📝 Обновлённые файлы

```
locust/
├── fastapi_main_uc01.py         ✅ + проверки производительности
├── fastapi_contact_uc02.py      ✅ + проверки производительности
├── fastapi_about_uc03.py        ✅ + проверки производительности
├── fastapi_projects_uc04.py     ✅ + проверки производительности
├── fastapi_contact_post_uc05.py 🆕 POST тесты формы и API
├── fastapi_metrics_uc06.py      🆕 тесты метрик
├── locustfile.py                ✅ + новые UC классы
├── loadshape_stability.py       ✅ + этапы для POST тестов
└── loadshape_performance.py     🆕 быстрый тест (3 минуты)
```

## 🎯 Сценарии использования

### 1. Продакшен мониторинг (БЕЗ POST тестов)

```bash
# В .env установи:
DISABLE_EMAIL=false

# Запусти только GET тесты
# (модифицируй loadshape, убрав UC05)
docker compose up
```

### 2. Тестирование производительности (С заглушкой)

```bash
# В .env установи:
DISABLE_EMAIL=true

# Запусти полный тест
docker compose up --build
```

### 3. Быстрая проверка (3 минуты)

```bash
# В .env установи:
DISABLE_EMAIL=true

# Запусти быстрый тест
docker compose -f docker-compose.performance.yml up --build
```

## 📊 Ожидаемые метрики

### При 50 одновременных пользователях:

- **GET /**
  - RPS: 150-200
  - P95: 40-60ms
  - P99: 80-100ms

- **GET /about, /projects, /contact**
  - RPS: 100-150
  - P95: 50-80ms
  - P99: 100-150ms

- **POST /contact**
  - RPS: 30-50
  - P95: 100-200ms (с заглушкой)
  - P99: 300-500ms

- **POST /api/contact**
  - RPS: 50-80
  - P95: 80-150ms (с заглушкой)
  - P99: 200-300ms

- **GET /metrics**
  - RPS: 200-300
  - P95: 10-20ms
  - P99: 30-50ms

## 🎉 Итог

✅ **7 Use Cases** с проверками производительности  
✅ **Автоматические assertions** на время ответа и статус коды  
✅ **Заглушка email** для избежания спама  
✅ **2 loadshape** - полный (5 минут) и быстрый (3 минуты)  
✅ **Готово к запуску** прямо сейчас!  

---

**🔥 Запускай и смотри метрики БЕЗ СПАМА на почту! 🔥**
