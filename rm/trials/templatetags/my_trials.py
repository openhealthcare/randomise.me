"""
Render the my trials table for a given user
"""
import datetime

from django import template

from rm.trials.models import Trial, Participant

td = datetime.date.today

register = template.Library()

@register.inclusion_tag('trials/dashboard.html', takes_context=True)
def my_trials(context):
    """
    Pass the trial queryset through to the table
    to be rendered.
    """
    user          = context['request'].user
    running       = Trial.objects.filter(owner=user)
    completed     = Trial.objects.completed().filter(owner=user)

    participated   = user.participant_set
    participating = participated.filter(trial__stopped=False)
    participated  = participated.filter(trial__stopped=True)



    return dict(running=running,
                completed=completed,
                participating=participating,
                participated=participated)
