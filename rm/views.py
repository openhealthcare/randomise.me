"""
Top level views for Randomise Me.

Static-ish pages etc.
"""
import random

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View
from letter.contrib.contact import ContactView, ReCaptchaContactForm

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
        context['request'] = self.request
        if self.request.user.is_authenticated():
            self.template_name = 'trials/my_trials.html'
            return context

        context['featured'] = Trial.objects.filter(featured=True)[:2]
        return context

class RMContactView(ContactView):
    """
    Pointless form for people who don't like their email clients
    """
    success_url = reverse_lazy('contact-ta')
    form_class  = ReCaptchaContactForm
