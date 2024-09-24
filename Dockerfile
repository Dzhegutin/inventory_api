FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY pyproject.toml .
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic



RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
