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
def create_a_trial_widget(context):
    """
    CTA to take the tutorial

    Return: dict
    Exceptions: None
    """
    return dict(show=True)

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




@register.inclusion_tag('dashboard/base.html', takes_context=True)
def my_trials(context):
    """
    Pass the trial queryset through to the table
    to be rendered.
    """
    user               = context['request'].user
    participated       = user.participant_set

    randomising_me = [Trial.objects.filter(owner=user, stopped=False, n1trial=True),
                       participated.filter(trial__stopped=False)]

    randomising_others = Trial.objects.filter(owner=user, stopped=False, n1trial=False)

    my_completed     = Trial.objects.filter(owner=user, stopped=True)

    participated   = participated.filter(trial__stopped=True)

    virgin = running.count() == 0 and completed.count() == 0 and participating.count() == 0 and participated.count() == 0


    return dict(virgin=virgin,
                running=running,
                completed=completed,
                participating=participating,
                participated=participated)
