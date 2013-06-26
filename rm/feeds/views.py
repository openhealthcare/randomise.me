"""
Syndication for Randomise Me.
"""
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from rm.trials.models import Trial


class TrialFeed(Feed):
    "Base trial feed"

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def items(self):
        return self.queryset[:20]


class LatestTrialsFeed(TrialFeed):
    """
    Feed for new trials as they are created.
    """
    title = "Randomise Me - New public trials"
    link = "/trials/past"
    description = "Latest new public trials on Randomise Me"
    queryset = Trial.objects.filter(private=False, stopped=False).order_by('-created')


class FinishedTrialsFeed(TrialFeed):
    """
    Feed for trials as they are stopped
    """
    title = "Randomise Me - Finished trials"
    link = "/trials/past"
    description = "Latest finished public trials on Randomise Me"
    queryset = Trial.objects.filter(private=False, stopped=True).order_by('-created')
