"""
The featured trials widget
"""
from django import template

from rm.trials.models import Trial

register = template.Library()

@register.inclusion_tag('trials/widgets/featured_trials.html', takes_context=False)
def featured_trials_widget(num):
    """
    Return a dictionary with the context for the
    Featured Trials Widget.

    This widget is a list of trials that have been editorially selected by
    the Randomise Me Team.

    Return: dict
    Exceptions: None
    """
    featured = Trial.objects.filter(featured=True)[:num]
    return dict(featured=featured)
