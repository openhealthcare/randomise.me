"""
Root URLs for Randomise.me
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from rm.trials.views import TrialSearchView, TutorialView, TutorialFromExampleView
from rm.views import HomeView, RMContactView
from rm.userprofiles.views import RMUserUpdate

from faq import views as faq_views

urlpatterns = patterns(
    '',
    # Boilerplates - not really our app.
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    # Accounts, profiles, login
    (r'^accounts/', include('allauth.urls')),
    # url(r'^cas/login/$', 'django_cas.views.login', name='cas-login'),
    # url(r'^cas/logout/$', 'django_cas.views.logout', name='cas-logout'),
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
    url(r'about$', TemplateView.as_view(template_name='about.html'),
        name='about-rm'),
    url(r'about-rcts$', TemplateView.as_view(template_name='rcts.html'),
        name='about-rcts'),
    url(r'how-do-rcts-work$',
        TemplateView.as_view(template_name='how-do-rcts-work.html'),
        name='how-do-rcts-work'),
    url(r'how-does-rm-work$',
        TemplateView.as_view(template_name='how-does-rm-work.html'),
        name='how-does-rm-work'),

    # Explicitly include only the FAQ views we want
    url(regex = r'faq$',
        view  = faq_views.TopicList.as_view(),
        name  = 'faq_topic_list',
    ),
    url(regex = r'faq/(?P<slug>[\w-]+)/$',
        view  = faq_views.TopicDetail.as_view(),
        name  = 'faq_topic_detail',
    ),
   url(regex = r'^(?P<topic_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        view  = faq_views.QuestionDetail.as_view(),
        name  = 'faq_question_detail',
    ),
#    url(r'dash$', MyTrials.as_view(), name='dash'),

    # profile editor
    url(r'account$', RMUserUpdate.as_view(), name='account-edit'),

    url(r'tutorial$', TutorialView.as_view(), name='tutorial'),
    url(r'tutorial/(?P<pk>\d+)$',
        TutorialFromExampleView.as_view(), name='tutorial-from-example'),

    # Trials on RM Users - CRUD routes
    url(r'^trials/', include('rm.trials.urls')),
    url(r'search$', TrialSearchView.as_view(), name='search'),

    url(r'^stats/', include('rm.stats.urls')),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
