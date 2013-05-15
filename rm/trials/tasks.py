"""
Celery tasks for the trials package
"""
import datetime
import time
from celery import task

from rm import exceptions
from rm.trials import models

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
    participant = models.Participant.objects.get(pk=participant_pk)
    participant.send_instructions()
    return True
