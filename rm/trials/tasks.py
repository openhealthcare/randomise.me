"""
Celery tasks for the trials package
"""
import datetime
import time
from celery import task

from rm import exceptions

td = lambda: datetime.date.today()


@task
def log():
    with open('/tmp/foo.log', 'a') as fh:
        fh.write("OH really? %s\n" % time.time())
        fh.flush()

@task
def email_rm_instructions():
    """
    Email instructions to participants of trials that are starting
    today.


    Return: None
    Exceptions: None
    """
    from rm.trials import models

    trials = models.Trial.objects.filter(instruction_date=td())
    for trial in trials:
        trial.send_instructions()
    return

@task
def instruct_later(participant_pk):
    """
    Email instructions to participants of trials that specified that
    this should be done X hours after randomisation
    """
    from rm.trials import models

    participant = models.Participant.objects.get(pk=participant_pk)
    participant.send_instructions()
    return True

@task
def close_dated_trials():
    """
    Look for trials that should close today and close them.

    Return: None
    Exceptions: None
    """
    from rm.trials.models import Trial
    for trial in Trial.objects.ending_today():
        trial.stop()
    return

@task
def randomise_me_reminder(pk):
    """
    Given the PK of a report, send the user a reminder if it
    still has no data left.


    Arguments:
    - `pk`: int

    Return:
    Exceptions:
    """
    from rm.trials.models import Report
    report = Report.objects.get(pk=pk)
    if report.date is None:
        report.send_reminder()
    return
