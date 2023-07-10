from django import template

register = template.Library()

@register.filter
def readable_date(value):
    return value.strftime('%d-%M-%Y')

@register.filter
def datetime_to_processable_date(value):
    return value.date().strftime('%Y-%m-%d') if value not in [''," ", None] else ""

@register.filter
def get_total_amount(value, arg):
    return value-arg

@register.filter
def add_numbers(value, args):
    return value+args

@register.filter
def return_array_from_csv(value):
    return value.split(',')
