"""
take a trial by ID and then fill it's participants and report their data as random variables

Only really useful to debug graphs
"""
import datetime
from optparse import make_option
import random
import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rm import exceptions
from rm.trials.models import Trial, Report

class Command(BaseCommand):
    """
    Our command.

    Nothing special to see here.
    """
    option_list = BaseCommand.option_list + (
        make_option('--primary_key', '-p', dest='pk',),
        )

    def handle(self, **options):
        trial = Trial.objects.get(pk=options['pk'])
        # Fill 'er up
        while trial.participant_set.count() < trial.min_participants:
            user = User.objects.get_or_create(
                username='fakeuser {0}'.format(time.time()))[0]
            trial.join(user)

        print trial.start_date, trial.finish_date
        if not trial.finished:
            delta = trial.time_remaining() - datetime.timedelta(days=1)
            trial.start_date -= delta
            trial.finish_date -= delta
            trial.save()

        try:
            trial.randomise()
        except exceptions.AlreadyRandomisedError:
            pass # Assume we're debugging

        for participant in trial.participant_set.all():
            start = trial.start_date
            while start <= trial.finish_date:
                score = random.randrange(1, 1000)
                print participant.user, start, score

                report = Report(trial=trial,
                                group=participant.group,
                                date=start,
                                score=score)
                report.save()
                start += datetime.timedelta(days=1)
