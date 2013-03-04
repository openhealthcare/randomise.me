from fabric.api import *
from fabric.colors import red, green

def manage(what):
    """
    Run a manage.py command
    """
    local('heroku run python manage.py {0}'.format(what))

@task
def deploy():
    """
    Make it so!
    """
    local('git push heroku master')
    manage('syncdb')
    manage('migrate')
