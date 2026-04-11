from django.conf import settings

from mysite.site_meta import get_site_last_updated_display, get_site_version


def site_settings(_request):
    """ค่าทั่วทั้งเว็บสำหรับเทมเพลต (ลิงก์สั่งซื้อ LINE เวอร์ชัน ฯลฯ)."""
    return {
        'LINE_ORDER_URL': getattr(
            settings,
            'LINE_ORDER_URL',
            'https://line.me/R/ti/p/@Dr.peakmaker',
        ),
        'SITE_VERSION': get_site_version(),
        'SITE_LAST_UPDATED_DISPLAY': get_site_last_updated_display(),
    }
