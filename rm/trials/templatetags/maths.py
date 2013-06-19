"""
Mathsy templatetags
"""
from django.template import Library

register = Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def percy(value):
    return '{0:.2}%'.format(value*100)
