"""
Render the my trials table for a given user
"""
from django import template

from rm.trials.models import Trial, Participant

register = template.Library()

@register.inclusion_tag('my_trials_table.html', takes_context=True)
def my_trials(context):
    """
    Pass the trial queryset through to the table
    to be rendered.
    """
    user = context['request'].user
    running = Trial.objects.filter(owner=user)
    participating = user.participant_set.all()
    return dict(running=running, participating=participating)
