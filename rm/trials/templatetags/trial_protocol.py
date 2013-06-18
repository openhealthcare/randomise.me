"""
The Trial Protocol Widget
"""
from django import template

from rm.trials.models import Trial

register = template.Library()

@register.inclusion_tag('trials/widgets/trial_protocol.html', takes_context=True)
def trial_protocol_widget(context):
    """
    Return a dictionary with the context for the
    Trial Protocol Widget.

    Return: dict
    Exceptions: None
    """
    ctx = context
    return ctx


@register.inclusion_tag('trials/widgets/trial_protocol_participant.html', takes_context=True)
def trial_protocol_participant_widget(context):
    """
    Return a dictionary with the context for the
    Trial Protocol_participant Widget.

    Return: dict
    Exceptions: None
    """
    ctx = context
    return ctx
