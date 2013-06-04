"""
Custom managers for Trials.
"""
import datetime

from django.db import models

td = lambda: datetime.date.today()

class RmTrialManager(models.Manager):

    def completed(self):
        """
        Return a queryset representing completed trials.

        Return: Queryset
        Exceptions: None
        """
        return self.filter(stopped=True)

    def recruiting(self):
        """
        Return a queryset representing the trials that are recruiting.

        Return: Queryset
        Exceptions: None
        """
        from rm.trials.models import Trial
        return self.filter(private=False, stopped=False, n1trial=False, recruitment=Trial.ANYONE)

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
        parent = self.get(**kwargs)
        trial.pk          = None
        trial.instruction_date = None
        trial.featured    = None
        trial.owner       = owner
        trial.parent      = parent
        return trial
