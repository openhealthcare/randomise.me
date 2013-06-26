from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from rm.feeds.views import LatestTrialsFeed, FinishedTrialsFeed

urlpatterns = patterns(
    '',
    url(r'^trials/new$', LatestTrialsFeed(), name='new-trials-feed'),
    url(r'^trials/finished$', FinishedTrialsFeed(), name='finished-trials-feed'),
    url(r'^$', TemplateView.as_view(template_name='feeds/index.html')),
)
