from datetime import datetime

from django import template

import locale

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

register = template.Library()


@register.simple_tag()
def current_time(format_string='%d %B %Y %I %H'):
    return datetime.utcnow().strftime(format_string)







