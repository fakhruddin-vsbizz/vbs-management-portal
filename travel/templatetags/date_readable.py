from django import template

register = template.Library()

@register.filter
def readable_date(value):
    return value.strftime('%d-%m-%Y')