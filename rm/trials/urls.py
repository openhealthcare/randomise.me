from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from rm.trials.views import (MyTrials, TrialCreateLanding,
                             TrialDetail, RandomiseMeView,
                             TrialCreate,
                             N1TrialCreate, ReproduceN1Trial,
                             TrialReport, JoinTrial,
                             EditTrial, TrialQuestion, StopTrial,
                             ToggleTrialPublicityView,
                             LeaveTrial, PeekTrial, InviteTrial,
                             ReproduceTrial, TrialAsCsvView,
                             AllTrials, FeaturedTrialsList,
                             ActiveTrialsView, PastTrialsView)
from rm.trials.views.offline import CreateOfflineTrialView

urlpatterns = patterns(
    '',
    url(r'my-trials$', MyTrials.as_view(), name='mytrials'),
    url(r'new$', TrialCreateLanding.as_view(), name='trial-create'),
    url(r'create$', TrialCreate.as_view(), name='rm-trial-create'),
    url(r'create-n1$', N1TrialCreate.as_view(), name='n1-trial-create'),
    url(r'n1/(?P<pk>\d+)/reproduce$', ReproduceN1Trial.as_view(),
        name='reproduce-n1-trial'),
    url(r'(?P<pk>\d+)$', TrialDetail.as_view(), name='trial-detail'),
    url(r'(?P<pk>\d+)/report', TrialReport.as_view(), name='trial-report'),
    url(r'(?P<pk>\d+)/question', TrialQuestion.as_view(), name='trial-question'),
    url(r'(?P<pk>\d+)/edit$', EditTrial.as_view(), name='edit-trial'),
    url(r'(?P<pk>\d+)/join$', JoinTrial.as_view(), name='join-trial'),
    url(r'(?P<pk>\d+)/stop$', StopTrial.as_view(), name='stop-trial'),
    url(r'(?P<pk>\d+)/toggle-publicity$', ToggleTrialPublicityView.as_view(),
        name='trial-toggle-public'),
    url(r'(?P<pk>\d+)/invite$', InviteTrial.as_view(), name='trial-invite'),
    url(r'(?P<pk>\d+)/peek$', PeekTrial.as_view(), name='trial-peek'),
    url(r'(?P<pk>\d+)/leave$', LeaveTrial.as_view(), name='leave-trial'),
    url(r'(?P<pk>\d+)/reproduce$', ReproduceTrial.as_view(),
        name='reproduce-trial'),
    url(r'(?P<pk>\d+)/as-csv$', TrialAsCsvView.as_view(), name='trial-as-csv'),
    url(r'(?P<pk>\d+)/randomise-me', RandomiseMeView.as_view(), name='randomise-me'),


    url(r'create-offline$', CreateOfflineTrialView.as_view(), name='create-offline-trial'),

    # Multiple ways to see lists of trials
    url(r'featured$', FeaturedTrialsList.as_view(), name='featured'),
    url(r'active$', ActiveTrialsView.as_view(), name='browse-active-trials'),
    url(r'past$', PastTrialsView.as_view(), name='browse-past-trials'),
    url(r'$', AllTrials.as_view(), name='trials'),

)
