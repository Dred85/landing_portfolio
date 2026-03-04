# 🔐 Настройка переменных окружения (.env)

## 📝 Добавь в .env файл

```env
# ========================================
# SMTP Настройки (для отправки email)
# ========================================
SMTP_SERVER=smtp.rambler.ru
SMTP_PORT=465
SMTP_USER=adrolv@rambler.ru
SMTP_PASS=<ваш_пароль_приложения>
SMTP_TO_EMAIL=adrolv@rambler.ru

# ========================================
# Настройки приложения
# ========================================
APP_NAME=Portfolio FastAPI
CONTACT_EMAIL=adrolv@rambler.ru

# ========================================
# Режим заглушки email
# ========================================
# DISABLE_EMAIL=false  # Продакшен - реальная отправка
# DISABLE_EMAIL=true   # Разработка/тесты - без отправки
```

## 🔧 Настройка для разных режимов

### 🏭 Продакшен (реальная отправка email)

```env
DISABLE_EMAIL=false
# или просто не устанавливать эту переменную
```

Запуск:
```bash
docker compose up
```

### 🧪 Тестирование (без спама)

```env
DISABLE_EMAIL=true
```

Запуск:
```bash
pytest  # Автоматически DISABLE_EMAIL=true
```

### 💻 Локальная разработка (без email)

```env
DISABLE_EMAIL=true
```

Запуск:
```bash
uvicorn app.main:app --reload
```

## 🎯 Как это работает

| Режим | DISABLE_EMAIL | Что происходит |
|-------|---------------|----------------|
| Тесты | `true` (авто) | ✅ Логирование, нет отправки |
| Разработка | `true` (опция) | ✅ Можно тестировать UI без SMTP |
| Продакшен | `false` или не установлено | 📧 Реальная отправка email |

## 🔍 Проверка в логах

### С заглушкой (DISABLE_EMAIL=true)
```
INFO | [ТЕСТОВЫЙ РЕЖИМ] Email не отправлен: {'name': 'Test User', ...}
```

### Без заглушки (реальная отправка)
```
INFO | Сообщение успешно отправлено: {'name': 'Test User', ...}
```

## 🚨 Важно!

- ⚠️  **Не коммить `.env` в git** (уже в `.gitignore`)
- 🔑 **Использовать пароль приложения** для Rambler SMTP
- ✅ **По умолчанию в тестах** заглушка включена автоматически

## 📌 Пример полного .env

```env
# Копируй этот шаблон в свой .env файл

SMTP_SERVER=smtp.rambler.ru
SMTP_PORT=465
SMTP_USER=adrolv@rambler.ru
SMTP_PASS=ТвойПарольПриложения123
SMTP_TO_EMAIL=adrolv@rambler.ru

APP_NAME=Portfolio FastAPI
CONTACT_EMAIL=adrolv@rambler.ru

# Для продакшена оставь закомментированным или false
# DISABLE_EMAIL=false

# Для разработки раскомментируй
# DISABLE_EMAIL=true
```

---

**Готово! Настрой `.env` и всё будет работать! 🎉**
