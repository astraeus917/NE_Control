from django import template
from datetime import datetime, date

register = template.Library()

@register.filter
def brl(value):
    """Formata número decimal como moeda brasileira"""
    try:
        return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value

@register.filter
def br_date(value):
    """Formata datas para o formato brasileiro: dd/mm/aaaa"""
    try:
        return value.strftime('%d/%m/%Y')
    except AttributeError:
        return value

@register.filter
def days_since(value):
    if not value:
        return ""
    today = date.today()
    diff = (today - value).days
    return abs(diff)  # força sempre positivo

