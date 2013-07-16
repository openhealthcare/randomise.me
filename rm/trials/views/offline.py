"""
Views related to offline trials.
"""
from django.views.generic import FormView

from rm.http import LoginRequiredMixin
from rm.trials.forms import OfflineTrialForm

class CreateOfflineTrialView(LoginRequiredMixin, FormView):
    """
    Create a trial with a dataset you already have.
    """
    form_class = OfflineTrialForm
    template_name = 'trials/offline/new.html'

    def form_valid(self, form):
        """
        If the form is valid, create the trial.

        Arguments:
        - `form`: OfflineTrialForm

        Return: ?
        Exceptions: None
        """
        return
