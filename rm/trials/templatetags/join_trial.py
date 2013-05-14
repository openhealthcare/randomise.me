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
    request = context['request']
    user = request.user
    recruiting = Trial.objects.recruiting()
    if user.is_authenticated():
        recruiting = recruiting.exclude(owner=user)
    return dict(recruiting=recruiting[:4])
