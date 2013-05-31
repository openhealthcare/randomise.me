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
        return self.filter()

    def completed(self):
        """
        Return a queryset representing completed trials.

        Return: Queryset
        Exceptions: None
        """
        return self.filter(stopped=True)

    def starting_today(self):
        """
        Return a queryset representing trials that start today.

        Return: Queryset
        Exceptions: None
        """
        return self.filter()


class SingleUserTrialManager(ActiveManager):
    pass

class RmTrialManager(ActiveManager):

    def recruiting(self):
        """
        Return a queryset representing the trials that are recruiting.

        Return: Queryset
        Exceptions: None
        """
        return self.active().filter(private=False, recruiting=True)

    def ending_today(self):
        """
        Return a queryset of those trials that are ending today.

        Return: Queryset
        Exceptions: None
        """
        from rm.trials.models import Trial
        return self.filter(ending_style=Trial.DATED, ending_date=td())

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
        trial.instruction_date = None
        trial.featured    = None
        trial.owner       = owner
        return trial
