"""
Celery tasks for the trials package
"""
import time
from celery import task

from rm import exceptions
from rm.trials import models

@task
def log():
    with open('/tmp/foo.log', 'a') as fh:
        fh.write("OH really? %s\n" % time.time())
        fh.flush()

@task
def email_single_instructions():
    """
    Email instructions to those users who are running trials on themselves.


    Return: None
    Exceptions: None
    """
    trials = models.SingleUserTrial.objects.active()
    for trial in trials:
        try:
            trial.send_instructions()
        except exceptions.NoEmailError:
            pass # Decide what to do here?
    return

@task
def email_rm_instructions():
    """
    Email instructions to participants of trials that are starting
    today.


    Return: None
    Exceptions: None
    """
    trials = models.Trial.objects.starting_today()
    for trial in trials:
        trial.randomise()
        trial.send_instructions()
    return
