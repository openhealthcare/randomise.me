"""
Helpers for sharing
"""
from django.template import Library

register = Library()

def absolute(request):
    return request.build_absolute_uri(request.path)

@register.inclusion_tag('share_this.html', takes_context=True)
def share_this(context):
    "What, you can't copy a URL? Bah."
    return dict(
        href=absolute(context['request']),
        img=context['request'].build_absolute_uri('/static/img/randomisemelogo.png')
        )

register.filter('absolute', absolute)