"""
Models for trials we're running
"""
import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from rm import exceptions
from rm.trials.validators import not_historic

class Trial(models.Model):
    """
    An individual trial that we are running.
    """
    SCORE  = 'sc'
    BINARY = 'bi'
    COUNT  = 'co'
    STYLE_CHOICES = (
        (SCORE,  'Score'),
        (BINARY, 'Binary'),
        (COUNT,  'Count')
        )

    HELP_URL = """This allows you to set a human-friendly url for your trial
so you can share nice links to it. If your url is set to 'awesome-trial' then
your trial will be available from randomise.me/awesome-trial. Valid characters
in your URL are letters, numbers underscores and hyphens. If you're into
regex, that's ([a-zA-Z0-9_-]+). You don't have to set a URL now, you can always
come back to it later. (Not implemented yet)"""
    HELP_DESC = """This is the explanatory text about your trial that will be
publically visible."""
    HELP_A = """These are the instructions that will be sent to Group A."""
    HELP_B = """These are the instructions thbt will be sent to Group B."""
    HELP_FINISH = "The date you would like your trial to finish (YYYY-MM-DD)"

    name              = models.CharField(max_length=200)
    # TODO Validate and implement this.
    url               = models.CharField(max_length=120,
                                         help_text=HELP_URL, blank=True, null=True)
    private           = models.BooleanField(default=False)
    style             = models.CharField(max_length=2, choices=STYLE_CHOICES)
    description       = models.TextField(help_text=HELP_DESC)
    group_a           = models.TextField(help_text=HELP_A)
    group_b           = models.TextField(help_text=HELP_B)
    min_participants  = models.IntegerField()
    max_participants  = models.IntegerField()
    group_a_expected  = models.IntegerField(blank=True, null=True)
    group_b_impressed = models.IntegerField(blank=True, null=True)
    finish_date       = models.DateField(help_text=HELP_FINISH,
                                         validators=[not_historic])
    finished          = models.BooleanField(default=False, editable=False)
    owner             = models.ForeignKey(User, editable=False)
    featured          = models.BooleanField(default=False)

    def __unicode__(self):
        """
        Nice printing representation
        """
        return '<{0}>'.format(self.name)

    def get_absolute_url(self):
        return reverse('trial-detail', kwargs={'pk': self.pk})

    def time_remaining(self):
        """
        How much time is between now and the end of the trial?
        """
        today = datetime.date.today()
        if self.finish_date < today:
            return 'Trial finished'
        return self.finish_date - today

    def can_join(self):
        """
        Predicate method to determine whether users are able to
        join this trial.

        We decide that a trial is unjoinable if it's finish date has
        passed, or if it's max participants limit has been met.
        """
        today = datetime.date.today()
        if self.finish_date < today:
            return False
        if self.participant_set.count() >= self.max_participants:
            return False
        return True

    def ensure_groups(self):
        """
        Ensure that the groups for this trial exist.
        """
        groupa = Group.objects.get_or_create(trial=self, name='a')[0]
        groupb = Group.objects.get_or_create(trial=self, name='b')[0]
        return groupa, groupb

    def join(self, user):
        """
        Add a user to our trial.

        Make sure that the trial has groups, then randomly assign USER
        to one of those groups.

        Ensure that we haven't gone over the max_participants level,
        raising TooManyParticipantsError if we have.

        Ensure that this user hasn't already joined the trial, raising
        AlreadyJoinedError if we have.

        Ensure that this user doesn't own the trial, raising
        TrialOwnerError if they do.

        If nobody has joined yet, we go to Group A, else Group A if
        the groups are equal, else Group B.
        """
        if self.owner == user:
            raise exceptions.TrialOwnerError()
        if Participant.objects.filter(trial=self, user=user).count() > 0:
            raise exceptions.AlreadyJoinedError()
        if self.participant_set.count() >= self.max_participants:
            raise exceptions.TooManyParticipantsError()
        groupa, groupb = self.ensure_groups()
        a_parts = groupa.participant_set.count()
        b_parts = groupb.participant_set.count()
        if a_parts == 0 or a_parts == b_parts:
            Participant(trial=self, group=groupa, user=user).save()
        else:
            Participant(trial=self, group=groupb, user=user).save()


class Group(models.Model):
    """
    The randomised groups of participants, automatically
    created for our trials
    """
    NAME_CHOICES = (
        ('A', 'Group A'),
        ('B', 'Group B')
        )
    trial = models.ForeignKey(Trial)
    name  = models.CharField(max_length=1, choices=NAME_CHOICES)


class Participant(models.Model):
    """
    A participant in a trial
    """
    user  = models.ForeignKey(User)
    trial = models.ForeignKey(Trial)
    group = models.ForeignKey(Group)

    def __unicode__(self):
        """
        Pretty printin'
        """
        return '<{0} - {1} ({2})>'.format(self.user, self.trial, self.group)
