"""
Render the reporting calendar for this trial
"""
import collections
import datetime

from django import template
from dateutil.relativedelta import relativedelta

register = template.Library()

Period = collections.namedtuple('Period', 'date reported future')

@register.inclusion_tag('trials/report_calendar_item.html', takes_context=True)
def report_cal(context):
    """
    Figure out a list of dicts representing each
    reporting period in this trial please.
    """
    trial, user = context['trial'], context['request'].user
    participant = trial.participant_set.get(user=user)
    reports = list(trial.report_set.filter(participant=participant))
    is_done = False
    if len(reports) > 0 and trial.reporting_style == trial.ONCE:
        is_done = True
    items = []
    start, end = participant.joined, participant.joined + datetime.timedelta(weeks=3)
    period_date = start

    delta = datetime.timedelta(days=1)
    if trial.reporting_freq == trial.WEEKLY:
        delta = datetime.timedelta(weeks=1)
    if trial.reporting_freq == trial.MONTHLY:
        delta = relativedelta(months=1)

    while period_date <= end:
        reported = any(map(lambda x: x.date==period_date, reports))
        period   = Period(period_date, reported, period_date > datetime.date.today())
        items.append(period)
        period_date += delta

    return dict(
        trial=trial,
        is_done=is_done,
        today=datetime.date.today(), # single reporting date
        items=items,                 # regular reporting periods
        )
