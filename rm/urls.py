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
from rm.trials.views import (MyTrials,
                             TrialDetail, TrialCreate, JoinTrial,
                             UserTrialCreate, UserTrialDetail, UserReport,
                             AllTrials, FeaturedTrialsList)

urlpatterns = patterns(
    '',
    # Boilerplates - not really our app.
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/'}),
    (r'^accounts/', include('allauth.urls')),

    # CAS login
    url(r'^cas/login/$', 'django_cas.views.login', name='cas-login'),
    url(r'^cas/logout/$', 'django_cas.views.logout', name='cas-logout'),


    # Pre - login
    url(r'^/?$', HomeView.as_view(), name='home'),
    url(r'account-types$', TemplateView.as_view(template_name='account_types.html'),
        name='account-types'),

    # Site-wide boilerplates - totally our app.
    url(r'disclaimer$', TemplateView.as_view(template_name='disclaimer.html'),
        name='disclaimer'),

    # Tabs at the top of a logged-in user's pages
    url(r'trials/my-trials$', MyTrials.as_view(), name='mytrials'),
    url(r'trials/new$', TemplateView.as_view(template_name='trials/new.html'),
        name='trial-create'),
    url(r'dash$', TemplateView.as_view(template_name='dash.html'), name='dash'),

    # Trials users run on themselves - CRUD routes
    url(r'trials/user/new', UserTrialCreate.as_view(), name='user-trial-create'),
    url(r'trials/user/(?P<pk>\d+)$', UserTrialDetail.as_view(), name='user-trial-detail'),
    url(r'trials/rm/(?P<pk>\d+)/report', UserReport.as_view(), name='user-trial-report'),

    # Trials on RM Users - CRUD routes
    url(r'trials/rm/new$', TrialCreate.as_view(), name='rm-trial-create'),
    url(r'trials/rm/(?P<pk>\d+)$', TrialDetail.as_view(), name='trial-detail'),
    url(r'trials/rm/(?P<pk>\d+)/join$', JoinTrial.as_view(), name='join-trial'),

    # Multiple ways to see lists of trials
    url(r'trials/featured$', FeaturedTrialsList.as_view(), name='featured'),
    url(r'trials$', AllTrials.as_view(), name='trials'),

)

urlpatterns += staticfiles_urlpatterns()
