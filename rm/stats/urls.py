from django.conf.urls import patterns, include, url

from rm.stats.views import PowerCalcView

urlpatterns = patterns(
    '',
    url(r'power-calc$', PowerCalcView.as_view(), name='power-calc'),
)
