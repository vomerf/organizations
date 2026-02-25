# Organizations API (FastAPI)

Тестовый API-сервис на FastAPI с PostgreSQL/PostGIS, Alembic и Docker.

## Стек

- FastAPI
- PostgreSQL + PostGIS
- SQLAlchemy (async)
- Alembic
- Docker / Docker Compose

## Быстрый старт (Docker)

1. Клонировать репозиторий и перейти в проект:

```bash
git clone <repo_url>
cd <project_dir>
```

2. Создать `.env`:

```bash
cp .env.example .env
```

3. Собрать образы:

```bash
docker compose build --no-cache
```

4. Запустить контейнеры:

```bash
docker compose up -d
```

Приложение будет доступно:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Миграции в контейнере

При старте `app` миграции выполняются автоматически (`alembic upgrade head`).

Если нужно накатить миграции вручную:

```bash
docker compose exec app alembic upgrade head
```

Проверить текущую ревизию:

```bash
docker compose exec app alembic current
```

## Заполнение таблиц тестовыми данными после миграций

После `alembic upgrade head` можно заполнить таблицы из `migration/seed_data.sql`:

```bash
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < migration/seed_data.sql
```

Скрипт очищает таблицы (`TRUNCATE ... RESTART IDENTITY CASCADE`) и загружает тестовые данные заново.

## Полезные команды

Остановить контейнеры:

```bash
docker compose down
```

Пересоздать БД с нуля (удалит volume с данными):

```bash
docker compose down -v
docker compose up -d --build
```
