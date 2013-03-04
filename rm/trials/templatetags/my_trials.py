"""
Render the my trials table for a given user
"""
from django import template

from rm.trials.models import Trial

register = template.Library()

@register.inclusion_tag('my_trials_table.html', takes_context=True)
def my_trials(context):
    """
    Pass the trial queryset through to the table
    to be rendered.
    """
#    with_status = [(t, t.status(user)) for t in context['trials']]
    user = context['request'].user
    trials = Trial.objects.filter(owner=user)
    return dict(trials=trials)
