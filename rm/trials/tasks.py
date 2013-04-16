"""
Celery tasks for the trials package
"""
import time
from celery import task

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
        trial.send_instructions()
    return
