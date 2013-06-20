from django.conf.urls import patterns, include, url

from rm.stats.views import PowerCalcView, PowerCalcBinaryView

urlpatterns = patterns(
    '',
    url(r'power-calc$', PowerCalcView.as_view(), name='power-calc'),
    url(r'power-calc-binary$', PowerCalcBinaryView.as_view(), name='power-calc-binary'),
)
