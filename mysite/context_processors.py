from django.conf import settings


def site_settings(_request):
    """ค่าทั่วทั้งเว็บสำหรับเทมเพลต (ลิงก์สั่งซื้อ LINE ฯลฯ)."""
    return {
        "LINE_ORDER_URL": getattr(
            settings,
            "LINE_ORDER_URL",
            "https://line.me/R/ti/p/@Dr.peakmaker",
        ),
    }
