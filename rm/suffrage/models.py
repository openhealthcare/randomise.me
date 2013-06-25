"""
Universal suffrage on models for django
"""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes import generic

class VotableMixin(object):
    """
    Mixin to add to models we wish to make votable.
    """
    def get_voting_url(self):
        """
        Return the url we should use to vote on this object
        """
        url_fmt = '/suffrage/{0}/{1}'
        return url_fmt.format(self.suffrage._content_id,
                              self.pk)

    @property
    def suffrage(instance):
        """
        Closure to get the instance.
        """
        class VoteManager(object):

            @property
            def _content_id(self):
                return ContentType.objects.get_for_model(instance).pk

            def _count_for(self, vote_direction):
                return Vote.objects.filter(val=vote_direction,
                                           content_type=self._content_id,
                                           object_id=instance.pk).count()

            @property
            def pluses(self):
                """
                Return the count of pluses for this model
                """
                return self._count_for(Vote.PLUS_ONE)

            @property
            def minuses(self):
                """
                Return the count of minuses for this model
                """
                return self._count_for(Vote.MINUS_ONE)

            @property
            def score(self):
                """
                Return the pluses - the minuses.
                """
                return self.pluses - self.minuses

            def vote_by(self, user):
                """
                Return the vote on this instance by USER or None
                """
                try:
                    return Vote.objects.get(voter=user,
                                            object_id=instance.pk,
                                            content_type=self._content_id)
                except Vote.DoesNotExist:
                    return None

        return VoteManager()


class Vote(models.Model):
    """
    Generic votes on Django models.
    """
    PLUS_ONE = +1
    MINUS_ONE = -1
    VOTE_CHOICES = (
        (PLUS_ONE, '+1'),
        (MINUS_ONE, '-1'),
        )

    val            = models.FloatField(choices=VOTE_CHOICES)
    content_type    = models.ForeignKey(ContentType)
    object_id      = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    voter          = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = (('voter', 'content_type', 'object_id'),)

    def __unicode__(self):
        return '{0} Vote on {1}'.format(self.get_vote_display(), self.content_object)
