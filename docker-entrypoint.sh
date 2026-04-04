#!/bin/sh
set -e
mkdir -p /app/media
if [ -n "$DJANGO_SQLITE_PATH" ]; then
  mkdir -p "$(dirname "$DJANGO_SQLITE_PATH")"
fi
python manage.py migrate --noinput
exec "$@"
