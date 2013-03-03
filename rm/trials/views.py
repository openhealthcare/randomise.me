"""
A create trial view?
"""
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from rm.trials.forms import TrialForm
from rm.trials.models import Trial

class TrialDetail(DetailView):
    """
    A trial detail page - this will be the unique URL for
    a trial.
    """
    context_object_name = "trial"
    model               = Trial

class TrialCreate(CreateView):
    """
    Create Me a trial please
    """
    context_object_name = "trial"
    model               = Trial
    form_class          = TrialForm

    def form_valid(self, form):
        """
        Add ownership details to the trial
        """
        form.instance.owner = self.request.user
        return super(TrialCreate, self).form_valid(form)
