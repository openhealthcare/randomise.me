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
    if my_trials.count() > 1:
        virgin = False

    context['virgin'] = virgin
    context['tutorial_prompt'] = tutorial_prompt
    return context

@register.inclusion_tag('trials/widgets/featured_trials.html', takes_context=False)
def featured_trials_full_widget(num):
    """
    Return a dictionary with the context for the
    Featured Trials Widget.

    This widget is a list of trials that have been editorially selected by
    the Randomise Me Team.

    Return: dict
    Exceptions: None
    """
    featured = Trial.objects.filter(featured=True)[:num]
    return dict(featured=featured)

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

@register.inclusion_tag('dashboard/new_offline_widget.html')
def new_offline_widget():
    """
    Widget to show on the new trials page
    """
    return {}

@register.inclusion_tag('dashboard/take_tutorial_widget.html')
def take_tutorial_widget():
    return {}

@register.inclusion_tag('dashboard/offline_tutorial_widget.html')
def offline_tutorial_widget():
    return {}

@register.inclusion_tag('dashboard/virgin_widget.html')
def virgin_widget():
    return {}


@register.inclusion_tag('dashboard/offline_soon_widget.html')
def offline_soon_widget():
    return {}

@register.inclusion_tag('dashboard/reports_part_widget.html', takes_context=True)
def reports_part_widget(context):
    user = context['request'].user
    participated = user.participant_set
    participated_over = [p.trial for p in participated.filter(trial__stopped=True)]
    num = len(participated_over)
    return dict(
        participated=participated_over,
        show=num > 0,
        num=num
        )

@register.inclusion_tag('dashboard/reports_ran_widget.html', takes_context=True)
def reports_ran_widget(context):
    user = context['request'].user
    over = Trial.objects.filter(owner=user, stopped=True, n1trial=False)
    num = over.count()
    return dict(
        participated=over,
        show=num > 0,
        num=num
        )

@register.inclusion_tag('trials/widgets/active_trials_widget.html', takes_context=True)
def active_trials_widget(context):
    """
    Widget for active trials before we move to full page active trials.
    """
    active = list(set(Trial.objects.filter(
        private=False,
        stopped=False,
        votes__isnull=False).exclude(hide=True).order_by('-votes__val')))[:7]
    return dict(active=active)

@register.inclusion_tag('trials/widgets/past_trials_widget.html', takes_context=True)
def past_trials_widget(context):
    """
    Widget for past trials before we move to full page past trials.
    """
    past = Trial.objects.filter(
        stopped=True, private=False,
        votes__isnull=False).exclude(
        hide=True).order_by(
        '-votes__val')[:7]
    return dict(past=past)

@register.inclusion_tag('trials/widgets/latest_trials_widget.html', takes_context=True)
def latest_trials_widget(context):
    """
    Widget for latest trials before we move to full page latest trials.
    """
    latest = Trial.objects.filter(
        offline=False,
        private=False).exclude(
        hide=True).order_by(
        '-created')[:7]
    return dict(latest=latest)
