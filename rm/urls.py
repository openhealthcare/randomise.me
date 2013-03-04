"""
Root URLs for Randomise.me
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from rm.trials.views import TrialDetail, TrialCreate, AllTrials, MyTrials

urlpatterns = patterns(
    '',
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'sign-up', TemplateView.as_view(template_name='sign_up.html'), name='signup'),
    url(r'trials/my-trials', MyTrials.as_view(), name='mytrials'),
    url(r'trials/new', TrialCreate.as_view(), name='trial-create'),
    url(r'trials/(?P<pk>\d+)$', TrialDetail.as_view(), name='trial-detail'),
    url(r'trials', AllTrials.as_view(), name='trials'),
    url(r'dash', TemplateView.as_view(template_name='dash.html'), name='dash'),
    url(r'disclaimer', TemplateView.as_view(template_name='disclaimer.html'), name='disclaimer'),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/'}),
    (r'^accounts/', include('allauth.urls')),

)

urlpatterns += staticfiles_urlpatterns()
