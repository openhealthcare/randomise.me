"""
Templatetag for the worked examples widget
"""
from django import template

from rm.trials.models import TutorialExample

register = template.Library()

@register.inclusion_tag('trials/worked_examples.html')
def worked_examples():
    """
    Return a dictionary containing a queryset with our worked examples.
    """
    return dict(examples=TutorialExample.objects.all())
