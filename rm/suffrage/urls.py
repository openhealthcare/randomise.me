from django.conf.urls import patterns, url

from rm.suffrage.views import VoteView

urlpatterns = patterns(
    '',
    url(r'^(?P<contenttype>\d+)/(?P<pk>\d+)$', VoteView.as_view(), name='voting'),
    )
