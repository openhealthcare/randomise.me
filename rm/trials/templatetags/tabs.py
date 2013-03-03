"""
Render our tabs with knowledge of which one is active
"""
from django import template

register = template.Library()

@register.inclusion_tag('tabs.html')
def tabs(active):
    """
    Pass the active variable to our tabs template
    """
    return dict(active=active)
