"""
Utilities for use in the randomise.me project
"""
import datetime

__all__ = [
    'today',
    'in_a',
    ]

_fmt = '%d/%m/%Y'

def today():
    """
    Return today's date as a string in the format
    DD/MM/YYYY

    Return: str
    Exceptions: None
    """
    return datetime.date.today().strftime(_fmt)

def in_a(week=None):
    """
    API for generating date strings at some
    point in the future relative to today.

    Arguments:
    - `week`: int

    Return: str
    Exceptions: None
    """
    td = datetime.date.today()
    future = td + datetime.timedelta(days=week*7)
    return future.strftime(_fmt)
