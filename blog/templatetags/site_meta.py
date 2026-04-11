from django import template

from mysite.site_meta import get_site_last_updated_display, get_site_version

register = template.Library()


@register.simple_tag
def site_version():
    return get_site_version()


@register.simple_tag
def site_last_updated():
    return get_site_last_updated_display()
