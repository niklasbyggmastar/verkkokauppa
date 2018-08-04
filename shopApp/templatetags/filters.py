from django import template
from django.db.models import Sum

register = template.Library()

@register.filter(name='sumOfList')  #is_safe?
def sumOfList(list):
    return len(list)
