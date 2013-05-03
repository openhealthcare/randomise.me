"""
Join a trial widget
"""
from django import template

from rm.trials.models import Trial

register = template.Library()

@register.inclusion_tag('trials/join_trial_widget.html', takes_context=True)
def join_trial_widget(context):
    """
    Render the join trial widget
    """
    return dict(recruiting=Trial.objects.recruiting()[:4])
