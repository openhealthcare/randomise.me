"""
Re-run the analysis for all trials.
Could take time.
Use sparingly in production.
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rm.trials.models import Trial, TrialAnalysis

class Command(BaseCommand):
    """
    Our command.

    Nothing special to see here.
    """
    def handle(self, **options):
        for trial in Trial.objects.filter(stopped=True):
            TrialAnalysis.report_on(trial)
            print trial
