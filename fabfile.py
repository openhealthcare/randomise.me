"""
Fabfile for Randomise Me
"""
from fabric.api import *
from fabric.colors import red, green

web = ['app@178.79.166.118']
#web = ['ohc@byta.randomizeme.org']
PROJ_DIR = '/home/app/randomise_me'
VENV_BIN = '/home/app/randomise_me/bin/{0}'
#PROJ_DIR = '/usr/local/ohc/'
#VENV_BIN = '/usr/local/ohc/rm/bin/{0}'
venv_bin = lambda x: VENV_BIN.format(x)
VENV_PY = venv_bin('python')
VENV_CTL = venv_bin('supervisorctl')

@hosts(web)
def mkenv():
    """
    Set up the directory environment required

    Return: None
    Exceptions: None
    """
    run('mkdir -p /usr/local/ohc/var/run')
    run('mkdir -p /usr/local/ohc/log/supervisord')


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

@hosts(web)
def start():
    """
    Start the application in production.
    """
    with cd(PROJ_DIR):
        supervisord = venv_bin('supervisord')
        run('{supervisord} -c etc/production.conf'.format(supervisord=supervisord))

@hosts(web)
def deploy():
    """
    Make it so!
    """
    with cd(PROJ_DIR):
        run('git pull origin master --tags') #not ssh - key stuff
        run('{0} install -r requirements.txt'.format(venv_bin('pip')))
        manage('collectstatic --noinput')
        migrate()
        restart()

@hosts(web)
def restart():
    """
    Restart the application
    """
    with cd(PROJ_DIR):
        supervisorctl('reread')
        supervisorctl('restart all')

@hosts(web)
def emergency():
    """
    Emergency rollback.
    """
    with cd(PROJ_DIR):
        run('git checkout stable')
        migrate()
        restart()
