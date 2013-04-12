"""
Utilities for use in the randomise.me project
"""
import datetime

__all__ = [
    'today',
    ]

def today():
    """
    Return today's date as a string in the format
    DD/MM/YYYY

    Return: str
    Exceptions: None
    """
    return datetime.date.today().strftime('%d/%m/%Y')
