from django import template
import locale

locale.setlocale(locale.LC_ALL, '')

register = template.Library()

@register.filter
def currency(value):
    try:
        value = int(value)
        return locale.format_string("%d", value, grouping=True)
    except (ValueError, TypeError):
        return value