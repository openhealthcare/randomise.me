"""
Root URLs for Randomise.me
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from rm.views import HomeView
from rm.trials.views import (TrialDetail, TrialCreate, AllTrials, MyTrials, JoinTrial,
                             FeaturedTrialsList)

urlpatterns = patterns(
    '',
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^/?$', HomeView.as_view(), name='home'),
    url(r'account-types$', TemplateView.as_view(template_name='account_types.html'),
        name='account-types'),
    url(r'trials/my-trials$', MyTrials.as_view(), name='mytrials'),
    url(r'trials/featured$', FeaturedTrialsList.as_view(), name='featured'),
    url(r'trials/new$', TrialCreate.as_view(), name='trial-create'),
    url(r'trials/(?P<pk>\d+)$', TrialDetail.as_view(), name='trial-detail'),
    url(r'trials/(?P<pk>\d+)/join$', JoinTrial.as_view(), name='join-trial'),
    url(r'trials$', AllTrials.as_view(), name='trials'),
    url(r'dash$', TemplateView.as_view(template_name='dash.html'), name='dash'),
    url(r'disclaimer$', TemplateView.as_view(template_name='disclaimer.html'),
        name='disclaimer'),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/'}),
    (r'^accounts/', include('allauth.urls')),

)

urlpatterns += staticfiles_urlpatterns()
