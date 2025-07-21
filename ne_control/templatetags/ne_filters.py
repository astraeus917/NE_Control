from django import template

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



