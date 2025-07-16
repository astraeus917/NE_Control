from django import template

register = template.Library()

@register.filter
def brl(value):
    """Formata número decimal como moeda brasileira"""
    try:
        return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value
