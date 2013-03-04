"""
Render our tabs with knowledge of which one is active
"""
from django import template

register = template.Library()

@register.inclusion_tag('tabs.html', takes_context=True)
def tabs(context, active):
    """
    Pass the active variable to our tabs template
    """
    return dict(active=active, user=context['request'].user)
