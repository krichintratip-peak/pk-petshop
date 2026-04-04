"""
Local development settings. Loads optional .env from project root.
Set DJANGO_SETTINGS_MODULE=mysite.settings.dev (or use mysite.settings package default).
"""

import os

from .base import *

try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

DEBUG = True

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-e(mbo5*%%mpoxfn$5=2pq%21f1!0p^ll7pl+%m=spox5ujyh-o',
)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
_extra_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if _extra_hosts:
    ALLOWED_HOSTS = list(
        {*ALLOWED_HOSTS, *[h.strip() for h in _extra_hosts.split(',') if h.strip()]}
    )
