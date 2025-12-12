FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
COPY backend/alembic.ini ./alembic.ini
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

ENV PYTHONPATH=/app

# Default environment; can be overridden at runtime (e.g. APP_ENV=production)
ENV APP_ENV=development

RUN chmod +x backend/entrypoint.sh

CMD ["backend/entrypoint.sh"]
