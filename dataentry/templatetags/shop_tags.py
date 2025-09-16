from django import template
from django.utils.html import format_html
from ..models import Employee

register = template.Library()

@register.simple_tag
def site_name():
    return "Automate with Django"



@register.simple_tag
def get_recent_products(count = 5):
    return Employee.objects.order_by('-salary')[:int(count)]


@register.filter(name='currency')
def currency(value, symbol='₹'):
    try:
        num = float(value)
    except (TypeError, ValueError):
        return value
    return f"{symbol}{num:,.2f}"


 
    