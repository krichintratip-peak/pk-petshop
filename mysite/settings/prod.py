"""
Production settings. Requires DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS.
Optional: POSTGRES_* (see base.py) for PostgreSQL; DJANGO_SQLITE_PATH for SQLite-only prod;
DJANGO_CSRF_TRUSTED_ORIGINS (comma-separated).
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

_sqlite_path = os.environ.get('DJANGO_SQLITE_PATH')
if _sqlite_path and not os.environ.get('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': Path(_sqlite_path).resolve(),
        }
    }

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('Set DJANGO_SECRET_KEY in the environment for production.')

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if h.strip()]
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        'Set DJANGO_ALLOWED_HOSTS to a comma-separated list of hostnames for production.'
    )

STATIC_ROOT = BASE_DIR / 'staticfiles'

if os.environ.get('DJANGO_ENABLE_WHITENOISE', '').lower() in ('1', 'true', 'yes'):
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

_csrf = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '')
if _csrf:
    CSRF_TRUSTED_ORIGINS = [x.strip() for x in _csrf.split(',') if x.strip()]

_secure = os.environ.get('DJANGO_USE_TLS', '1').lower() in ('1', 'true', 'yes')
if _secure:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
