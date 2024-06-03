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

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def add(value, arg):
    """Adds the arg to the value."""
    return value + arg