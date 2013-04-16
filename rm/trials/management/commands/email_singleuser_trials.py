"""
Force email those SingleUserTrials that are active today with their instructions.

Only really useful in development or breakage scenarios.
"""
from django.core.management.base import BaseCommand

from rm.trials import tasks

class Command(BaseCommand):
    """
    Our command.

    Nothing special to see here.
    """
    def handle(self, **options):
        tasks.email_single_instructions()
