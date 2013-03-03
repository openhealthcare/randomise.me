"""
Models for trials we're running
"""
import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

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
    ASAP = 'as'
    HOUR = 'ho'
    DATE = 'dr'
    INSTRUCT_STYLE_CHOICES = (
        (ASAP, 'As soon as they can'),
        (HOUR, 'X hours after joining'),
        (DATE, 'On this date and time')
        )

    name              = models.CharField(max_length=200)
    url               = models.CharField(max_length=120, unique=True)
    private           = models.BooleanField(default=False)
    question          = models.TextField()
    style             = models.CharField(max_length=2, choices=STYLE_CHOICES)
    description       = models.TextField()
    group_a           = models.TextField()
    group_b           = models.TextField()
    instruct_style    = models.CharField(max_length=2, choices=INSTRUCT_STYLE_CHOICES)
    instruct_hour     = models.IntegerField(blank=True, null=True)
    instruct_date     = models.DateTimeField(blank=True, null=True)
    min_participants  = models.IntegerField()
    max_participants  = models.IntegerField()
    group_a_expected  = models.IntegerField()
    group_b_impressed = models.IntegerField()
    finish_date       = models.DateField()
    finished          = models.BooleanField(default=False, editable=False)
    owner             = models.ForeignKey(User, editable=False)

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
