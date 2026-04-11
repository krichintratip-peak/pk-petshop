"""เวอร์ชันและวันอัปเดตล่าสุด — ใช้ใน settings, context processor และ template tags."""

from __future__ import annotations

from datetime import date

from django.conf import settings


def format_last_updated_thai_be(d: date | None) -> str:
    """แสดงเป็น dd-mm-yyyy โดยปี พ.ศ."""
    if d is None:
        return ''
    year_be = d.year + 543
    return f'{d.day:02d}-{d.month:02d}-{year_be}'


def get_site_version() -> str:
    return getattr(settings, 'SITE_VERSION', '0.0.0')


def get_site_last_updated_display() -> str:
    last = getattr(settings, 'SITE_LAST_UPDATED', None)
    if isinstance(last, str) and last.strip():
        parts = last.strip().split('-')[:3]
        if len(parts) == 3:
            y, m, d = (int(x) for x in parts)
            last = date(y, m, d)
        else:
            last = None
    if isinstance(last, date):
        return format_last_updated_thai_be(last)
    return ''
