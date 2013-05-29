"""
MODELS for trials we're running
"""
import datetime
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
import letter

from rm import exceptions
from rm.trials import managers, tasks

td = lambda: datetime.date.today()
POSTIE = letter.DjangoPostman()
Avg = models.Avg
User = get_user_model()


class Trial(models.Model):
    """
    An individual trial that we are running.
    """
    ANYONE     = 'an'
    INVITATION = 'in'
    RECRUITMENT_CHOICES = (
        (ANYONE,     'Anyone can join'),
        (INVITATION, "Only people I've invited can join")
        )

    IMMEDIATE = 'im'
    HOURS     = 'ho'
    DATE      = 'da'
    INSTRUCTION_CHOICES = (
        (IMMEDIATE, 'Straight away after randomisation'),
        (HOURS, 'X hours after randomisation'),
        (DATE, 'On this date...')
        )

    DAILY   = 'da'
    WEEKLY  = 'we'
    MONTHLY = 'mo'
    FREQ_CHOICES = (
        (DAILY,   'Once per day'),
        (WEEKLY,  'Once per week'),
        (MONTHLY, 'Once per month')
        )

    HELP_PART = """Who can participate in this trial?
(Everyone? People with an infant under 6 months? People who binge drink Alcohol?)"""
    HELP_A = """These are the instructions that will be sent to the group who
get the intervention"""
    HELP_B = """These are the instructions that will be sent to the control group"""
    HELP_START = "The date you would like your trial to start"
    HELP_FINISH = "The date you would like your trial to finish"

    # Step 1
    title          = models.CharField(max_length=200, blank=True, null=True)

    # Step 2
    reporting_freq = models.CharField("Reporting frequency", max_length=200,
                                      choices=FREQ_CHOICES, default=DAILY)

    # Step 3
    min_participants  = models.IntegerField("I think I need a minimum of x participants for a meaningful answer")

    # Step 4
    recruitment       = models.CharField(max_length=2, choices=RECRUITMENT_CHOICES,
                                         default=ANYONE)

    # Step 5
    description       = models.TextField(blank=True, null=True)
    group_a_desc      = models.TextField("Intervention Group description", blank=True, null=True)
    group_b_desc      = models.TextField("Control Group description", blank=True, null=True)
    # Step 6
    group_a           = models.TextField("Intervention Group Instructions", help_text=HELP_A)
    group_b           = models.TextField("Control Group Instructions", help_text=HELP_B)
    instruction_delivery = models.TextField(max_length=2, choices=INSTRUCTION_CHOICES,
                                            default=IMMEDIATE)
    instruction_hours_after = models.IntegerField(blank=True, null=True)
    instruction_date = models.DateField(blank=True, null=True)

    group_a_expected  = models.IntegerField(blank=True, null=True)
    group_b_impressed = models.IntegerField(blank=True, null=True)
    start_date        = models.DateField(help_text=HELP_START)
    finish_date       = models.DateField(help_text=HELP_FINISH)
    stopped          = models.BooleanField(default=False)
    owner             = models.ForeignKey(settings.AUTH_USER_MODEL)
    featured          = models.BooleanField(default=False)
    recruiting        = models.BooleanField(default=True)
    participants      = models.TextField(help_text=HELP_PART, blank=True, null=True)
    is_edited         = models.BooleanField(default=False)

#    created           = models.DateTimeField(default=lambda: datetime.datetime.now(), blank=tr)
    private           = models.BooleanField(default=False)
    objects = managers.RmTrialManager()

    def __unicode__(self):
        """
        Nice printing representation
        """
        return '<{0}>'.format(self.title)

    def get_absolute_url(self):
        return reverse('trial-detail', kwargs={'pk': self.pk})

    def save(self):
        """
        Check for recruiting status

        Return: None
        Exceptions: None
        """
        self.recruiting = self.can_join()
        return super(Trial, self).save()

    def results(self):
        """
        Return the results of this trial

        Return: dict
        Exceptions: None
        """
        avg = lambda g: self.report_set.filter(
            group__name=g).aggregate(Avg('score')).values()[0]

        intervention_group = avg('A')
        control_group = avg('B')
        return [dict(name='Intervention Group', avg=intervention_group),
                dict(name='Control Group', avg=control_group)]


    @property
    def started(self):
        """
        Property to determine whether this trial has started or not.

        Return: bool
        Exceptions: None
        """
        if self.start_date is None:
            return False
        if self.start_date <= datetime.date.today():
            return True
        return False

    @property
    def finished(self):
        """
        Predicate property to determine whether this trial is finished.

        Return: bool
        Exceptions: None
        """
        if self.stopped:
            return True
        if self.finish_date < td():
            return True
        return False

    @property
    def active(self):
        """
        Property to determine whether this trial is active today.

        Return: bool
        Exceptions: None
        """
        if not self.start_date or not self.finish_date:
            return False
        if self.start_date <= td() and self.finish_date >= td():
            return True
        return False

    @property
    def is_invitation_only(self):
        """
        Predicate property to determine whether the trial
        is invitation_only.

        Return: None
        Exceptions: None
        """
        return self.recruitment == self.INVITATION

    def related(self):
        """
        Get trials possibly related to this one.

        Return: Queryset
        Exceptions: None
        """
        return Trial.objects.exclude(pk=self.pk)[:5]

    def time_remaining(self):
        """
        How much time is between now and the end of the trial?

        Return: timedelta or str
        Exceptions: None
        """
        if self.finish_date < td():
            return 'finished'
        return self.finish_date - td()

    def can_join(self):
        """
        Predicate method to determine whether users are able to
        join this trial.

        We decide that a trial is unjoinable if it's finish date has
        passed, or if it's max participants limit has been met.
        """
        if self.finish_date < td():
            return False
        return True

    def needs(self):
        """
        How many participants does this trial need?

        Return: bool
        Exceptions: None
        """
        return (self.min_participants - self.participant_set.count() )

    def needs_participants(self):
        """
        Does this trial need participants?

        Return: bool
        Exceptions: None
        """
        return self.needs() > 0

    def ensure_groups(self):
        """
        Ensure that the groups for this trial exist.
        """
        groupa = Group.objects.get_or_create(trial=self, name=Group.GROUP_A)[0]
        groupb = Group.objects.get_or_create(trial=self, name=Group.GROUP_B)[0]
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

        Ensure that this trial isn't already finished, raising
        TrialFinishedError if it is.

        If nobody has joined yet, we go to Group A, else Group A if
        the groups are equal, else Group B.
        """
        if self.owner == user:
            raise exceptions.TrialOwnerError()
        today = datetime.date.today()
        if self.finish_date < today:
            raise exceptions.TrialFinishedError()
        if Participant.objects.filter(trial=self, user=user).count() > 0:
            raise exceptions.AlreadyJoinedError()
        if self.participant_set.count() >= self.max_participants:
            raise exceptions.TooManyParticipantsError()
        part = Participant(trial=self, user=user).randomise()
        part.save()
        if self.instruction_delivery == self.IMMEDIATE:
            part.send_instructions()
        if self.instruction_delivery == self.HOURS:
            eta = datetime.utcnow() + datetime.timedelta(seconds=60*60*self.instruction_hours_after)
            tasks.instruct_later.apply_async((participant.pk), eta=eta)
        return

    def randomise(self):
        """
        Randomise the participants of this trial.

        If we have already randomised the participants, raise AlreadyRandomisedError.

        Return: None
        Exceptions: AlreadyRandomisedError
        """
        if self.participant_set.filter(group__isnull=False).count() > 0:
            raise exceptions.AlreadyRandomisedError()
        groupa, groupb = self.ensure_groups()
        for participant in self.participant_set.all():
            participant.group = random.choice([groupa, groupb])
            participant.save()
        return

    def send_instructions(self):
        """
        Email the participants of this trial with their instructions.

        Return: None
        Exceptions:
            - TrialFinishedError: The trial has finished
            - TrialNotStartedError: The trial is yet to start
        """
        if self.start_date is not None and self.start_date > td():
            raise exceptions.TrialNotStartedError()
        if self.finish_date is not None and self.finish_date < td():
            raise exceptions.TrialFinishedError()
        for participant in self.participant_set.all():
            participant.send_instructions()
        return


class Invitation(models.Model):
    """
    An email we've invited to a trial.
    """
    trial = models.ForeignKey(Trial)
    email = models.EmailField(max_length=254)
    sent  = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0} - {1}'.format(self.email, self.trial.title)

    def invite(self):
        """
        Send an invitation email to this invitee.

        Return: None
        Exceptions: None
        """
        subject = 'Invitation to participate in {0}'.format(self.trial.title)
        class Message(letter.Letter):
            Postie   = POSTIE

            From     = settings.DEFAULT_FROM_EMAIL
            To       = self.email;
            Subject  = subject
            Template = 'email/rm_invitation'
            Context  = {
                'href'        : settings.DEFAULT_DOMAIN + self.trial.get_absolute_url(),
                'owner'       : self.trial.owner,
                'name'        : self.trial.title
                }

        Message.send()
        self.sent = True
        self.save()
        return


class Variable(models.Model):
    """
    A variable that we are reporting on
    """
    SCORE  = 'sc'
    BINARY = 'bi'
    COUNT  = 'co'

    STYLE_CHOICES = (
        (SCORE,  'Score'),
        (BINARY, 'Binary'),
        (COUNT,  'Count')
        )

    trial = models.ForeignKey(Trial)
    name  = models.CharField(max_length=200, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    style = models.CharField(max_length=2, choices=STYLE_CHOICES)

    def __unicode__(self):
        return '<Variable {0} ({1})>'.format(self.name, self.style)

    def report_form(self):
        """
        Return the relevant report form with this as it's
        instance.

        Return: Form
        Exceptions: None
        """
        from rm.trials import forms
        data = dict(
            trial=self.trial,
            variable=self
            )
        return forms.reportform_factory(self, data)


class Group(models.Model):
    """
    The randomised groups of participants, automatically
    created for our trials
    """
    GROUP_A = 'A'
    GROUP_B = 'B'
    NAME_CHOICES = (
        (GROUP_A, 'Group A'),
        (GROUP_B, 'Group B')
        )

    trial = models.ForeignKey(Trial)
    name  = models.CharField(max_length=1, choices=NAME_CHOICES)

    def __unicode__(self):
        return self.name

class Participant(models.Model):
    """
    A participant in a trial
    """
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    trial = models.ForeignKey(Trial)
    group = models.ForeignKey(Group, blank=True, null=True)

    def __unicode__(self):
        """
        Pretty printin'
        """
        return '<{0} - {1} ({2})>'.format(self.user, self.trial, self.group)

    def randomise(self):
        """
        Randomise this participant into a group

        Return: Participant
        Exceptions: None
        """
        self.group = random.choice(self.trial.ensure_groups())
        self.save()
        return self

    def send_instructions(self):
        """
        Email the participant their instructions for this trial.

        If the participant does not have an email address, raise an error.

        Return: None
        Exceptions: NoEmailError
        """
        if not self.user.email:
            raise exceptions.NoEmailError()

        subject = 'Randomise.me - instructions for {0}'.format(self.trial.title)
        instructions = self.group.name == 'A' and self.trial.group_a or self.trial.group_b
        question = self.trial.variable_set.all()[0].question

        class Message(letter.Letter):
            Postie   = POSTIE

            From     = settings.DEFAULT_FROM_EMAIL
            To       = self.user.email
            Subject  = subject
            Template = 'email/rm_instructions'
            Context  = {
                'href'        : settings.DEFAULT_DOMAIN + self.trial.get_absolute_url(),
                'instructions': instructions,
                'name'        : self.trial.title,
                'frequency'   : self.trial.get_reporting_freq_display(),
                'question'    : question
                }

        Message.send()
        return


class Report(models.Model):
    "A report of a single datapoint for a trial"

    trial        = models.ForeignKey(Trial)
    participant  = models.ForeignKey(Participant, blank=True, null=True)
    group        = models.ForeignKey(Group, blank=True, null=True)
    date         = models.DateField()
    variable     = models.ForeignKey(Variable)
    score        = models.IntegerField(blank=True, null=True)
    binary       = models.NullBooleanField(blank=True)
    count        = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return '<Report for {0} {1} on {2}>'.format(self.trial.title,
                                                    getattr(self.group, 'name', 'noname'),
                                                    self.date)

    def get_absolute_url(self):
        return reverse('trial-detail', kwargs={'pk': self.trial.pk})
