"""
Render a trial Call To Action for a given trial/user combo
"""
from django import template

from rm.trials.models import Trial, Participant

register = template.Library()

@register.inclusion_tag('trials/trial_cta.html')
def trial_cta(trial, user):
    """
    Figure out the user's relationship to the trial
    """
    participating, owner = False, False
    if user.is_authenticated():
        participating = trial.participant_set.filter(user=user).count() > 0
        owner = trial.owner == user

    return dict(owner=owner, participating=participating, trial=trial)
