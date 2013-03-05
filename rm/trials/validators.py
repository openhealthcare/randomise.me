"""
Trial validators
"""
import datetime

from django.core.exceptions import ValidationError

def not_historic(value):
    """
    Validate that a particular date is not in the past.
    """
    today = datetime.date.today()
    if value < today :
        raise ValidationError('{0} is in the past'.format(value))
