import time
from celery import task

@task
def log():
    with open('/tmp/foo.log', 'a') as fh:
        fh.write("%s\n" % time.time())
