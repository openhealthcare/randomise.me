"""
Root URLs for Randomise.me
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from rm.trials.views import TrialSearchView
from rm.views import HomeView, RMContactView
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
    url(r'^glossary/', include('terms.urls')),

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


#    url(r'dash$', MyTrials.as_view(), name='dash'),

    # profile editor
    url(r'account$', RMUserUpdate.as_view(), name='account-edit'),

    url(r'tutorial',
        TemplateView.as_view(template_name='trials/tutorial.html'),
        name='tutorial'),

    # Trials on RM Users - CRUD routes
    url(r'^trials/', include('rm.trials.urls')),
    url(r'search$', TrialSearchView.as_view(), name='search'),

)

urlpatterns += staticfiles_urlpatterns()
