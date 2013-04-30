"""
Top level views for Randomise Me.

Static-ish pages etc.
"""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from rm.trials.models import Trial

class HomeView(TemplateView):
    """
    The front page of the site for anonymous users
    """
    template_name='home.html'

    def get_context_data(self, **kw):
        """
        Add featured trials for the homepage
        """
        context = super(HomeView, self).get_context_data(**kw)
        context['recruiting'] = Trial.objects.recruiting()[:4]
        context['finished'] = Trial.objects.filter(finished=True, featured=True)[:2]
        return context
