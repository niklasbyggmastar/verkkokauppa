from django import template

register = template.Library()

@register.filter(name='range')  #is_safe?
def filter_range(start,end):
    return range(start,end)
