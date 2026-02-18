FROM python:3.12-slim

RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

COPY pyproject.toml poetry.lock* /project/

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY migration /project/migration
COPY alembic.ini /project/
COPY app /project/app

# порт
EXPOSE 8000

# запуск
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]