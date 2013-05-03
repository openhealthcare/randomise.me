"""
Custom managers for Trials.
"""
import datetime

from django.db import models

td = lambda: datetime.date.today()

class ActiveManager(models.Manager):
    """
    Custom manager for single user trials.

    Mostly API sugar
    """

    def active(self):
        """
        Return a queryset representing currently active trials.

        Return: Queryset
        Exceptions: None
        """
        return self.filter(start_date__lte=td(), finish_date__gte=td())

    def starting_today(self):
        """
        Return a queryset representing trials that start today.

        Return: Queryset
        Exceptions: None
        """
        return self.filter(start_date=td())



class SingleUserTrialManager(ActiveManager):
    pass

class RmTrialManager(ActiveManager):

    def recruiting(self):
        """
        Return a queryset representing the trials that are recruiting.

        Return: Queryset
        Exceptions: None
        """
        return self.filter(finished=False, private=False, recruiting=True)

    def reproduce(self, owner, **kwargs):
        """
        Return a cleaned version of a trial to reproduce.

        Arguments:
        - `**kwargs`: {}

        Return: Trial
        Exceptions: None
        """
        trial = self.get(**kwargs)
        trial.pk          = None
        trial.start_date  = None
        trial.finish_date = None
        trial.featured    = None
        trial.owner       = owner
        return trial
