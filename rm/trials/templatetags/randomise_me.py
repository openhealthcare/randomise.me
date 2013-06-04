"""
The randomise Me widget for a particular trial.
"""
from django import template

register = template.Library()

@register.inclusion_tag('trials/randomise_me_widget.html', takes_context=True)
def randomise_me_widget(context):
    """
    Return a dictionary with the context for the
    Randomise Me Widget.

    This widget is a button that will assign the owner into a group
    on demand, as well as a form / display for all previous demanded
    randomisations.

    Arguments:
    - `context`: Context

    Return: dict
    Exceptions: None
    """
    trial = context['trial']
    reports = trial.report_set.all()
    pending = None
    active_instructions = None
    if reports.filter(date__isnull=True).count() > 1:
        pending = reports.filter(date__isnull=True)[0]
        if pending.group == pending.group.GROUP_A:
            active_instructions = trial.group_a
        else:
            active_instructions = trial.group_b

    return {
        'trial': trial,
        'reports': reports,
        'pending': pending,
        'active_instructions': active_instructions,
        }
