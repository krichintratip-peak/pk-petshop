FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Postgres driver: ติดตั้งใน image (Linux wheel) — ไม่ใส่ใน requirements.txt เพื่อให้ dev บน Windows ใช้ SQLite ได้โดยไม่ต้องมีไดรเวอร์
RUN pip install -r requirements.txt && pip install "psycopg2-binary==2.9.10"

COPY docker-entrypoint.sh /docker-entrypoint.sh
# Windows CRLF ทำให้ exec entrypoint ล้ม (no such file or directory) — บังคับ LF
RUN sed -i 's/\r$//' /docker-entrypoint.sh && chmod +x /docker-entrypoint.sh

COPY . .

# Build-time only: collectstatic needs valid prod env
ARG DJANGO_SECRET_KEY=build-only-collectstatic
ARG DJANGO_ALLOWED_HOSTS=localhost
ENV DJANGO_SETTINGS_MODULE=mysite.settings.prod \
    DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
    DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS \
    DJANGO_USE_TLS=0 \
    DJANGO_ENABLE_WHITENOISE=1

RUN python manage.py collectstatic --noinput

# Runtime must set secrets via env / docker.env
ENV DJANGO_SECRET_KEY="" \
    DJANGO_ALLOWED_HOSTS=""

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "120"]
