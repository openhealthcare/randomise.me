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
import numpy as np
from scipy import stats as scistats
from sorl import thumbnail
from statsmodels.stats.power import tt_ind_solve_power

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
    ON_DEMAND = 'de'
    INSTRUCTION_CHOICES = (
        (IMMEDIATE, 'Straight away after randomisation'),
        # (HOURS, 'X hours after randomisation'),
        (DATE, 'On this date...'),
        (ON_DEMAND, 'On Demand')
        )

    ONCE      = 'on'
    WHENEVER  = 'wh'
    DATED     = 'da'
    REGULARLY = 're'

    REPORT_STYLE_CHOICES = (
#        (ONCE,      'Once only'),
        (WHENEVER,  'Whenever they want'),
        (DATED,     'On date x'),
        # (REGULARLY, 'Regularly')
        )

    DAILY   = 'da'
    WEEKLY  = 'we'
    MONTHLY = 'mo'

    FREQ_CHOICES = (
        (DAILY,   'Once per day'),
        (WEEKLY,  'Once per week'),
        (MONTHLY, 'Once per month')
        )


    MANUALLY = 'ma'
    REPORT_NUM = 're'
    ENDING_CHOICES = (
        (MANUALLY, 'Manually'),
        (REPORT_NUM, 'After X have reported'),
        (DATED, 'On date Y')
        )

    HELP_PART = """Who can participate in this trial?
(Everyone? People with an infant under 6 months? People who binge drink Alcohol?)"""
    HELP_A = """These are the instructions that will be sent to group A"""
    HELP_B = """These are the instructions that will be sent to group B"""

    # Step 1
    title          = models.CharField(max_length=200, blank=True, null=True)

    # Step 2
    reporting_style = models.CharField("Reporting Style", max_length=2,
                                       choices=REPORT_STYLE_CHOICES, default=WHENEVER)
    reporting_freq = models.CharField("Reporting frequency", max_length=2,
                                      choices=FREQ_CHOICES, default=DAILY)
    reporting_date = models.DateField('Reporting date', blank=True, null=True)

    # Step 3
    min_participants  = models.IntegerField(
        "I think I need a minimum of x participants for a meaningful answer")

    # Step 4
    recruitment       = models.CharField(max_length=2, choices=RECRUITMENT_CHOICES,
                                         default=ANYONE)

    # Step 5
    description       = models.TextField(blank=True, null=True)
    image             = thumbnail.ImageField(upload_to='uploads', blank=True, null=True)
    secret_info       = models.TextField(blank=True, null=True)

    # Step 6
    group_a           = models.TextField("Group A Instructions", help_text=HELP_A)
    group_b           = models.TextField("Group B Instructions", help_text=HELP_B)
    instruction_delivery = models.CharField(max_length=2, choices=INSTRUCTION_CHOICES,
                                            default=IMMEDIATE)
    instruction_hours_after = models.IntegerField(blank=True, null=True)
    instruction_date = models.DateField(blank=True, null=True)

    # Step 7
    ending_style   = models.CharField(max_length=2, choices=ENDING_CHOICES, default=MANUALLY)
    ending_reports = models.IntegerField(blank=True, null=True)
    ending_date    = models.DateField(blank=True, null=True)


    # Currently unused power calcs
    group_a_expected  = models.IntegerField(blank=True, null=True)
    group_b_impressed = models.IntegerField(blank=True, null=True)

    # Metadata
    owner             = models.ForeignKey(settings.AUTH_USER_MODEL)
    n1trial           = models.BooleanField(default=False)
    featured          = models.BooleanField(default=False)
    stopped           = models.BooleanField(default=False)
    is_edited         = models.BooleanField(default=False)
    created           = models.DateTimeField(default=lambda: datetime.datetime.now())
    private           = models.BooleanField(default=False)
    parent            = models.ForeignKey('self', blank=True, null=True,
                                          related_name='child')

    # Currently unused advanced user participants
    participants      = models.TextField(help_text=HELP_PART, blank=True, null=True)


    objects = managers.RmTrialManager()

    def __unicode__(self):
        """
        Nice printing representation
        """
        return '#({0}) {1}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse('trial-detail', kwargs={'pk': self.pk})

    def save(self):
        """
        Check for recruiting status

        Return: None
        Exceptions: None
        """
        if self.recruitment == self.INVITATION:
            self.private = True
        return super(Trial, self).save()

    def image_url(self):
        """
        Return the url for SELF.image or None

        Return: str or None
        Exceptions: None
        """
        if not self.image:
            return
        return settings.MEDIA_URL + self.image.file.name.split('/')[-1]


    def results(self):
        """
        Return the results of this trial

        Return: dict
        Exceptions: None
        """
        anal = self.trialanalysis_set.get()
        return [dict(name='Group A', avg=anal.meana),
                dict(name='Group B', avg=anal.meanb)]


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

    def main_outcome(self):
        """
        Return the trial's main outcome
        """
        try:
            return self.variable_set.all()[0]
        except IndexError:
            return []

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
        return 'No longer appropriate'

    def can_join(self):
        """
        Predicate method to determine whether users are able to
        join this trial.

        We decide that a trial is unjoinable if it's finish date has
        passed, or if it's max participants limit has been met.
        """
        if self.stopped == True or self.n1trial == True:
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

        Ensure that this user hasn't already joined the trial, raising
        AlreadyJoinedError if we have.

        Ensure that this trial isn't already finished, raising
        TrialFinishedError if it is.

        If nobody has joined yet, we go to Group A, else Group A if
        the groups are equal, else Group B.
        """
        if self.stopped:
            raise exceptions.TrialFinishedError()
        if Participant.objects.filter(trial=self, user=user).count() > 0:
            raise exceptions.AlreadyJoinedError()
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
        # if self.start_date is not None and self.start_date > td():
        #     raise exceptions.TrialNotStartedError()
        if self.stopped:
            raise exceptions.TrialFinishedError()
        for participant in self.participant_set.all():
            participant.send_instructions()
        return

    def stop(self):
        """
        Stop this trial please.

        Return: None
        Exceptions: None
        """
        self.stopped = True
        self.save()
        TrialAnalysis.report_on(self)
        for participant in self.participant_set.exclude(user=self.owner):
            participant.send_ended_notification()
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
    style = models.CharField(max_length=2, choices=STYLE_CHOICES, default=SCORE)
    image = thumbnail.ImageField(upload_to='variableuploads', blank=True, null=True)

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

    def duplicate(self):
        """
        Return a new variable un-linked to this trial

        Return: Variable
        Exceptions: None
        """
        return Variable(name=self.name, question=self.question, style=self.style)


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
    joined = models.DateField(default=lambda: datetime.date.today(), blank=True)

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
                'group'       : self.group.name,
                'question'    : question
                }

        self.user.send_message(Message)
        return

    def send_ended_notification(self):
        """
        Send an email notification to participants of a trial when
        it's been stopped.

        Return: None
        Exceptions: None
        """
        subject = 'Randomise Me - Trial {0} has ended'.format(self.trial.title)
        class Message(letter.Letter):
            Postie   = POSTIE

            From     = settings.DEFAULT_FROM_EMAIL
            To       = self.user.email
            Subject  = subject
            Template = 'email/rm_ended'
            Context  = {
                'href'        : settings.DEFAULT_DOMAIN + self.trial.get_absolute_url(),
                'name'        : self.trial.title,
                }

        self.user.send_message(Message)
        return


class Report(models.Model):
    "A report of a single datapoint for a trial"

    trial        = models.ForeignKey(Trial)
    participant  = models.ForeignKey(Participant, blank=True, null=True)
    group        = models.ForeignKey(Group, blank=True, null=True)
    date         = models.DateField(blank=True, null=True)
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

    def reported(self):
        """
        Predicate method to determine whether this report instance
        has already reported data.

        Return: bool
        Exceptions: None
        """
        if self.variable.style == Variable.SCORE and self.score is not None:
            return True
        if self.variable.style == Variable.BINARY and self.binary is not None:
            return True
        if self.variable.style == Variable.COUNT and self.count is not None:
            return True
        return False

    def get_value(self):
        """
        Return the value of this report according to the style or None.
        """
        if self.variable.style == Variable.SCORE:
            return self.score
        if self.variable.style == Variable.BINARY:
            return self.binary
        if self.variable.style == Variable.COUNT:
            return self.count
        return

    def send_reminder(self):
        """
        Send a reminder email to our participant that
        they randomised themselves.

        Return: None
        Exceptions: None
        """
        user = self.participant.user
        subject = 'We recently randomised you...'
        question = self.trial.variable_set.all()[0].question

        class Message(letter.Letter):
            Postie   = POSTIE

            From     = settings.DEFAULT_FROM_EMAIL
            To       = user.email
            Subject  = subject
            Template = 'email/rm_reminder'
            Context  = {
                'href'        : settings.DEFAULT_DOMAIN + self.trial.get_absolute_url(),
                'group'       : self.group.name,
                'question'    : question,
                'name'       : self.trial.title
                }

        user.send_message(Message)
        return



class TutorialExample(models.Model):
    """
    Pre-filled examples for the tutorial.
    """
    SCORE  = 'sc'
    BINARY = 'bi'
    COUNT  = 'co'

    STYLE_CHOICES = (
        (SCORE,  'Score'),
        (BINARY, 'Binary'),
        (COUNT,  'Count')
        )

    name = models.CharField(max_length=200)
    question = models.CharField(max_length=200)
    measure_style = models.CharField(max_length=2, choices=STYLE_CHOICES, default=SCORE)
    measure_question = models.TextField()
    group_a = models.TextField()
    group_b = models.TextField()

    def get_absolute_url(self):
        return reverse('tutorial-from-example', kwargs={'pk': self.pk})


class TrialAnalysis(models.Model):
    """
    Cache of report info for a stopped trial
    """
    trial = models.ForeignKey(Trial)
    power_small = models.FloatField(blank=True, null=True)
    power_med = models.FloatField(blank=True, null=True)
    power_large = models.FloatField(blank=True, null=True)
    mean = models.FloatField(blank=True, null=True)
    sd = models.FloatField(blank=True, null=True)
    nobsa = models.IntegerField(blank=True, null=True)
    nobsb = models.IntegerField(blank=True, null=True)
    meana = models.FloatField(blank=True, null=True)
    meanb = models.FloatField(blank=True, null=True)
    stderrmeana = models.FloatField(blank=True, null=True)
    stderrmeanb = models.FloatField(blank=True, null=True)

    @staticmethod
    def report_on(trial):
        """
        Calculate headline stats for TRIAL once
        """
        nobs1 = int(trial.report_set.count()/2)
        reports = trial.report_set.exclude(date__isnull=True)
        points = [t.get_value() for t in reports]
        pointsa = [t.get_value() for t in reports.filter(group__name=Group.GROUP_A)]
        pointsb = [t.get_value() for t in reports.filter(group__name=Group.GROUP_B)]
        sd = np.std(points)
        mean = np.mean(points)

        nobsa = len(pointsa)
        nobsb = len(pointsb)
        meana = np.mean(pointsa)
        meanb = np.mean(pointsb)
        stderrmeana = scistats.sem(pointsa)
        stderrmeanb = scistats.sem(pointsb)

        small = tt_ind_solve_power(effect_size=0.1, alpha=0.05, nobs1=nobs1, power=None)
        med = tt_ind_solve_power(effect_size=0.2, alpha=0.05, nobs1=nobs1, power=None)
        large = tt_ind_solve_power(effect_size=0.5, alpha=0.05, nobs1=nobs1, power=None)
        tr = TrialAnalysis.objects.get_or_create(trial=trial)[0]

        tr.power_small=small
        tr.power_med=med
        tr.power_large=large
        tr.sd=sd
        tr.mean=mean
        tr.nobsa = nobsa
        tr.nobsb = nobsb
        tr.meana = meana
        tr.meanb = meanb
        tr.stderrmeana = stderrmeana
        tr.stderrmeanb = stderrmeanb

        tr.save()
        return
