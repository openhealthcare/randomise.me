"""
Render the my trials table for a given user
"""
import datetime
import itertools

from django import template
from faq.models import Question

from rm.trials.models import Trial, Participant, TutorialExample

td = datetime.date.today

register = template.Library()

@register.inclusion_tag('dashboard/base.html', takes_context=True)
def dashboard(context):
    """
    Top level dashboard tag

    Return: dict
    Exceptions: None
    """
    user               = context['request'].user
    my_trials = Trial.objects.filter(owner=user)

    virgin = True
    tutorial_prompt = True
    # if my_trials.count() > 1:
    #     virgin = False
    #     if my_trials.count() > 4:
    #         tutorial_prompt = False

    context['virgin'] = virgin
    context['tutorial_prompt'] = tutorial_prompt
    return context


@register.inclusion_tag('dashboard/randomising_me_widget.html', takes_context=True)
def randomising_me_widget(context):
    """
    List of trials randomising this user

    Return: dict
    Exceptions: None
    """
    user               = context['request'].user
    participated       = user.participant_set

    randomising_me = set(list(itertools.chain(
            Trial.objects.filter(owner=user, stopped=False, n1trial=True),
            [p.trial for p in participated.filter(trial__stopped=False)]
            )))

    num = len(randomising_me)
    if num > 0:
        return dict(randomising_me=randomising_me,
                    num=num,
                    show=True)
    return dict(show=False)


@register.inclusion_tag('dashboard/randomising_others_widget.html', takes_context=True)
def randomising_others_widget(context):
    """
    List of trials randomising this user

    Return: dict
    Exceptions: None
    """
    user               = context['request'].user
    randomising_others = Trial.objects.filter(owner=user, stopped=False, n1trial=False)

    if randomising_others.count() > 0:
        return dict(randomising_others=randomising_others, show=True,
                    num=randomising_others.count())
    return dict(show=False)


@register.inclusion_tag('dashboard/create_a_trial_widget.html', takes_context=True)
def create_a_trial_widget(context, size=False):
    """
    CTA to take the tutorial

    Return: dict
    Exceptions: None
    """
    return dict(show=True, size=size)

@register.inclusion_tag('dashboard/example_trials_widget.html', takes_context=True)
def example_trials_widget(context):
    """
    CTA to take the tutorial

    Return: dict
    Exceptions: None
    """
    return dict(
        show=True,
        examples=TutorialExample.objects.all()
        )

@register.inclusion_tag('dashboard/did_you_know_widget.html', takes_context=True)
def did_you_know_widget(context):
    """
    CTA to take the tutorial

    Return: dict
    Exceptions: None
    """
    return dict(
        show=True,
        faq=Question.objects.all()[:4]
        )

@register.inclusion_tag('dashboard/featured_trials_widget.html', takes_context=True)
def featured_trials_widget(context):
    """
    Widget to show people trials we like

    Return: dict
    Exceptions: None
    """
    featured = Trial.objects.filter(featured=True)[:2]
    return dict(featured=featured)

@register.inclusion_tag('dashboard/new_nof1_widget.html')
def new_nof1_widget():
    """
    Widget to show on the new trials page
    """
    return {}

@register.inclusion_tag('dashboard/new_trial_widget.html')
def new_trial_widget():
    """
    Widget to show on the new trials page
    """
    return {}


@register.inclusion_tag('dashboard/take_tutorial_widget.html')
def take_tutorial_widget():
    return {}
