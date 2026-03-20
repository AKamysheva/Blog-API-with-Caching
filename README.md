# API для блога с кэшированием постов

#### Функциональность

- CRUD для постов:
    - ```GET /posts``` — получить список постов
    - ```GET /posts/{post_id}``` — получить пост
    - ```POST /posts/create-post``` — создать пост
    - ```PUT /posts/update-post/{id}``` — обновить пост
    - ```DELETE /posts/delete-post/{id}``` — удалить пост
- Кэширование

  Реализовано кэширование для эндпоинта: ```GET /posts/{post_id}```
  
  Применяется паттерн Cache-Aside (Ленивая загрузка)
  
  Логика:
   - Проверка наличия поста в Redis
   - Если есть → вернуть из кеша 
   - Если нет → взять из PostgreSQL, сохранить в Redis.
   При изменении или удалении поста, сначала обновляется БД/удаляется запись из БД, затем удаление происходит из кэша.
   По умолчанию TTL = 600 секунд (10 минут).

## Stack
- Backend: Python, FastAPI
- Cache: Redis
- Database: PostgreSQL
- ORM: SQLAlchemy
- Dependency manager: Poetry

## Необходимые технологии
- Python 3.13
- Poetry
- Docker and Docker Compose (optional)

## Установка
1. Клонируем репозиторий:
   ```
   git clone https://github.com/AKamysheva/Blog-API-with-Caching.git
   poetry install 
   ```
2. Создать .env файл в папке ```app```
   ```
   POSTGRES_USER=myuser
   POSTGRES_PASSWORD=mypassword
   POSTGRES_DB=mydatabase
   HOST_DB=db
   PORT_DB=5432
   REDIS_HOST=redis
   REDIS_PORT=6379
   REDIS_DB=0
   CACHE_TTL=600
   ```
3. Запускаем проект с Docker Compose:
   ```
   docker build -t system_with_cache .
   docker compose up -d
   ```

## Тестирование
Тесты запускаются с помощью pytest и поддерживают асинхронные проверки через pytest‑asyncio.
Покрывают основные сценарии работы кеша: сохранение данных в Redis, а также инвалидацию кеша 
при обновлении и удалении постов.
```
poetry run pytest
```

## API Documentation
👉 http://localhost:8400/docs
