<<<<<<< HEAD
Описание API
=======
# Organizations API (FastAPI)

Test project with:

* FastAPI
* PostgreSQL
* SQLAlchemy (async)
* Alembic
* Docker

## Run with Docker

1. Clone repository

```
git clone <repo_url>
cd project
```

2. Create environment file

```
cp .env.example .env
```

3. Run containers

```
docker compose up --build
```

API will be available at:

* http://localhost:8000
* Swagger: http://localhost:8000/docs

## Migrations

Migrations are applied automatically on container start:

```
alembic upgrade head
```

## Stack

* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Alembic
* Docker / Docker Compose
>>>>>>> b87f3fa (add docker file)
