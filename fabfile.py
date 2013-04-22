"""
Fabfile for Randomise Me
"""
from fabric.api import *
from fabric.colors import red, green

web = ['ohc@byta.randomizeme.org']
PROJ_DIR = '/usr/local/ohc/randomise.me'
VENV_BIN = '/home/ohc/.virtualenvs/rm/bin/{0}'
venv_bin = lambda x: VENV_BIN.format(x)
VENV_PY = venv_bin('python')
VENV_CTL = venv_bin('supervisorctl')

def manage(what):
    """
    Run a manage.py command

    Return: None
    Exceptions: None
    """
    with cd(PROJ_DIR):
        run('{0} manage.py {1}'.format(VENV_PY, what))

def supervisorctl(what):
    """
    Run a supervisorctl command

    Arguments:
    - `what`: the command to run

    Return: None
    Exceptions: None
    """
    run('{ctl} {what}'.format(ctl=VENV_CTL, what=what))

def migrate():
    """
    Update the database
    """
    manage('syncdb --migrate')

def stop():
    """
    Stop the application in production
    """
    run("kill -9 `cat /usr/local/ohc/var/run/supervisord.pid`")
#    supervisorctl('stop')
    # with cd(PROJ_DIR):
        # run('pkill gunicorn || echo "Gunicorn not running"')
        # run("ps auxww | grep celery | grep -v grep| awk '{print $2}'| xargs kill -9 || echo 'Celery not running'")


def start():
    """
    Start the application in production.
    """
    with cd(PROJ_DIR):
        supervisord = venv_bin('supervisord')
        run('{supervisord} -c etc/production.conf'.format(supervisord=supervisord))
        # run('{0} -D -c gunicorn_conf.py'.format(venv_bin('gunicorn_django')))
        # manage('celery worker --scheduler=djcelery.schedulers.DatabaseScheduler -B')
#        manage('celerybeat -S djcelery.schedulers.DatabaseScheduler')

@hosts(web)
def deploy():
    """
    Make it so!
    """
    with cd(PROJ_DIR):
        run('git pull origin master') #not ssh - key stuff
        run('{0} install -r requirements.txt'.format(venv_bin('pip')))
        migrate()
        restart()


@hosts(web)
def restart():
    """
    Restart the application
    """
    supervisorctl('reread')
    supervisorctl('restart all')
