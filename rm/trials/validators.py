"""
Trial validators
"""
import datetime

from django.core.exceptions import ValidationError

from rm.trials import models

def not_historic(value):
    """
    Validate that a particular date is not in the past.
    """
    today = datetime.date.today()
    if value < today :
        raise ValidationError('{0} is in the past'.format(value))
    return True

def during_trial(value, start_date, finish_date):
    """
    Validate that the VALUE is during the boundaries of TRIAL

    Arguments:
    - `value`: date
    - `trial`: BaseTrial

    Return: bool
    Exceptions: ValidationError
    """
    if value < start_date:
        raise ValidationError('{0} was before the trial started'.format(value))
    if value > finish_date:
        raise ValidationError('{0} is after the trial finished'.format(value))
    return True

def no_single_report(value, trial):
    """
    Validate that there is not already a report for VALUE

    Arguments:
    - `value`: date
    - `trial`: BaseTrial

    Return: bool
    Exceptions: ValidationError
    """
    if models.SingleUserReport.objects.filter(trial=trial, date=value).count() > 0:
        raise ValidationError('Already reported data for {0}'.format(value))
    return True
