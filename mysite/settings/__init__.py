"""
Django settings package.

- Default import path ``mysite.settings`` uses development settings (dev.py).
- Production: set ``DJANGO_SETTINGS_MODULE=mysite.settings.prod`` (e.g. in wsgi deployment).
"""

from .dev import *
