"""
Utilities for Trials
"""
from rm.trials.models import Trial

def n1_with_sane_defaults(owner, title, group_a, group_b):
    """
    Create A N=1 trial with sane defaults

    Useful for Easy mode / the Tutorial

    Arguments:
    - `owner`: RMUser
    - `title`: str
    - `group_a`: str
    - `group_b`: str

    Return: Trial
    Exceptions: None
    """
    description = 'This Trial, {0} was created with the Randomise Me \
tutorial...'.format(title)

    trial = Trial(
        title=title,
        reporting_style=Trial.WHENEVER,
        min_participants=1,
        recruitment=Trial.ANYONE,
        description=description,
        group_a=group_a,
        group_b=group_b,
        instruction_delivery=Trial.ON_DEMAND,
        owner=owner,
        n1trial=True,
        private=True
        )
    trial.save()
    trial.join(owner)
    return trial
