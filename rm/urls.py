"""
Root URLs for Randomise.me
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from rm.views import HomeView, RMContactView
from rm.trials.views import (MyTrials,
                             TrialDetail, TrialCreate, TrialReport, JoinTrial,
                             ReproduceTrial, TrialAsCsv,
                             UserTrialCreate, UserTrialDetail, UserReport,
                             AllTrials, FeaturedTrialsList, TrialSearchView)
from rm.userprofiles.views import RMUserUpdate

urlpatterns = patterns(
    '',
    # Boilerplates - not really our app.
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),

    # Accounts, profiles, login
    (r'^accounts/', include('allauth.urls')),
    url(r'^cas/login/$', 'django_cas.views.login', name='cas-login'),
    url(r'^cas/logout/$', 'django_cas.views.logout', name='cas-logout'),
    url(r'^profile/', include('rm.userprofiles.urls')),

    # Payment
    url(r'^gocardless/', include('rm.gcapp.urls')),

    # Pre - login
    url(r'^/?$', HomeView.as_view(), name='home'),
    url(r'account-types$', TemplateView.as_view(template_name='account_types.html'),
        name='account-types'),

    # Site-wide boilerplates - totally our app.
    url(r'disclaimer$', TemplateView.as_view(template_name='disclaimer.html'),
        name='disclaimer'),
    url(r'contact$', RMContactView.as_view(), name='contact'),
    url(r'contact-ta$', TemplateView.as_view(template_name='contact-ta.html'),
        name='contact-ta'),

    # Static content pages
    url(r'about$', TemplateView.as_view(template_name='about.html'), name='about-rm'),
    url(r'about-rcts$', TemplateView.as_view(template_name='rcts.html'), name='about-rcts'),
    url(r'how-do-rcts-work$', TemplateView.as_view(template_name='how-do-rcts-work.html'), name='how-do-rcts-work'),

    # Tabs at the top of a logged-in user's pages
    url(r'trials/my-trials$', MyTrials.as_view(), name='mytrials'),
    url(r'trials/new$', TemplateView.as_view(template_name='trials/new.html'),
        name='trial-create'),
#    url(r'dash$', TemplateView.as_view(template_name='dash.html'), name='dash'),
    url(r'dash$', MyTrials.as_view(), name='dash'),

    # profile editor
    url(r'account$', RMUserUpdate.as_view(), name='account-edit'),

    # Trials users run on themselves - CRUD routes
    url(r'trials/user/new', UserTrialCreate.as_view(), name='user-trial-create'),
    url(r'trials/user/(?P<pk>\d+)$', UserTrialDetail.as_view(), name='user-trial-detail'),
    url(r'trials/user/(?P<pk>\d+)/report', UserReport.as_view(), name='user-trial-report'),
    url(r'tutorial',
        TemplateView.as_view(template_name='trials/tutorial.html'),
        name='tutorial'),

    # Trials on RM Users - CRUD routes
    url(r'trials/rm/new$', TrialCreate.as_view(), name='rm-trial-create'),
    url(r'trials/rm/(?P<pk>\d+)$', TrialDetail.as_view(), name='trial-detail'),
    url(r'trials/rm/(?P<pk>\d+)/report', TrialReport.as_view(), name='trial-report'),
    url(r'trials/rm/(?P<pk>\d+)/join$', JoinTrial.as_view(), name='join-trial'),
    url(r'trials/rm/(?P<pk>\d+)/reproduce$', ReproduceTrial.as_view(),
        name='reproduce-trial'),
    url(r'trials/rm/(?P<pk>\d+)/as-csv$', TrialAsCsv.as_view(), name='trial-as-csv'),

    # Multiple ways to see lists of trials
    url(r'trials/featured$', FeaturedTrialsList.as_view(), name='featured'),
    url(r'trials$', AllTrials.as_view(), name='trials'),
    url(r'search$', TrialSearchView.as_view(), name='search')

)

urlpatterns += staticfiles_urlpatterns()
