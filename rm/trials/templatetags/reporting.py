"""
Reporting forms &tc
"""
import datetime

from django import template

register = template.Library()

@register.inclusion_tag('trials/reporting/base.html', takes_context=True)
def reporting_widget(context):
    """
    Given TRIAL, render the appropriate reporting widget
    """
    trial, user = context['trial'], context['request'].user

    participant = trial.participant_set.get(user=user)
    reports = list(trial.report_set.filter(participant=participant))
    is_done = False

    if len(reports) > 0 and trial.reporting_style == trial.ONCE:
        widget_template = 'trials/reporting/is_done.html'
    elif trial.reporting_style == trial.DATED:
        widget_template = 'trials/reporting/dated.html'
    elif trial.reporting_style == trial.REGULARLY:
        widget_template = 'trials/reporting/regularly.html'
    elif trial.reporting_style == trial.WHENEVER:
        widget_template = 'trials/reporting/whenever.html'
    else:
        widget_template = 'trials/reporting/once.html'

    return dict(
        trial=trial,
        reports=reports,
        widget_template=widget_template,
        today = datetime.date.today()
        )
