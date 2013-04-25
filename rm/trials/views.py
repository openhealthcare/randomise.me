"""
A create trial view?
"""
import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, View, ListView
from django.views.generic.edit import CreateView

from rm import exceptions
from rm.trials.forms import (TrialForm, TrialReportForm, UserTrialForm,
                             UserReportForm)
from rm.trials.models import Trial, Report, SingleUserTrial, SingleUserReport
from django.utils import simplejson

class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )

class LoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ReportView(CreateView):
    """
    Generic report data view.

    Ensures that we have access to the right trial at the right time.
    """

    context_object_name = 'report'

    def get(self, *args,**kw):
        """
        Store the trial isntance
        """
        self.trial = self.trial_model.objects.get(pk=kw['pk'])
        return super(ReportView, self).get(*args, **kw)

    def post(self, *args,**kw):
        """
        Store the trial isntance
        """
        self.trial = self.trial_model.objects.get(pk=kw['pk'])
        return super(ReportView, self).post(*args, **kw)

    def get_context_data(self, **kw):
        """
        We want access to the trial data in the template please!
        """
        trial = getattr(self, 'trial', None)
        if not trial:
            raise ValueError()
        context = super(ReportView, self).get_context_data(**kw)
        context['trial'] = trial
        return context

    def get_form(self, *args, **kwargs):
        """
        Add the trial to the instance
        """
        trial = getattr(self, 'trial', None)
        form = super(ReportView, self).get_form(*args, **kwargs)
        form.instance.trial = trial
        return form

    def form_valid(self, form):
        """
        We need to update the report object to set the trial
        and figure out the group that the user was allocated
        to on the date in question.
        """
        trial = getattr(self, 'trial', None)
        if not trial:
            raise ValueError()
        form.instance.trial = trial
        return super(ReportView, self).form_valid(form)



# Views for user tabs

class MyTrials(TemplateView):
    """
    Trials associated with this user
    """
    template_name = 'trials/my_trials.html'

# Views for trials on RM users.

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


class JoinTrial(LoginRequiredMixin, TemplateView):
    """
    Allow a user to join a trial
    """
    template_name = 'trials/join_trial.html'

    def __init__(self, *args, **kwargs):
        """
        Add an errors container
        """
        self.errors = []
        super(JoinTrial, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        trial = Trial.objects.get(pk=kwargs['pk'])
        self.trial = trial
        return super(JoinTrial, self).get(self, *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Join the trial!
        """
        trial = Trial.objects.get(pk=kwargs['pk'])
        self.trial = trial
        user = self.request.user
        try:
            trial.join(user)
        except exceptions.TooManyParticipantsError:
            self.errors.append('Too many participants on this trial already')
        except exceptions.AlreadyJoinedError:
            self.errors.append('You were already participating in this trial!')
        except exceptions.TrialOwnerError:
            self.errors.append('This is your trial - joining it would be wonky!')
        except exceptions.TrialFinishedError:
            self.errors.append('This trial has already finished!')
        return super(JoinTrial, self).get(self, * args, **kwargs)

    def get_context_data(self, **kw):
        """
        We'd like access to the trial in our joined template
        """
        context = super(JoinTrial, self).get_context_data(**kw)
        context['errors'] = self.errors
        context['trial']  = self.trial
        return context

class TrialReport(ReportView):
    """
    Report a data point for this trial
    """
    model       = Report
    trial_model = Trial
    form_class  = TrialReportForm

# Views for trials users run on themselves
class UserTrialCreate(LoginRequiredMixin, CreateView):
    """
    Let's make a trial!
    """
    context_object_name = 'trial'
    model               = SingleUserTrial
    form_class          = UserTrialForm

    def form_valid(self, form):
        """
        Add ownership details to the trial
        """
        form.instance.owner = self.request.user
        return super(UserTrialCreate, self).form_valid(form)


class UserReport(ReportView):
    """
    Report a single data point for this trial
    """
    model       = SingleUserReport
    trial_model = SingleUserTrial
    form_class  = UserReportForm


class UserTrialDetail(DetailView):
    """
    View the details of a single user trial
    """
    context_object_name = 'trial'
    model               = SingleUserTrial


# Views for trial discovery - lists, featured, etc.

class AllTrials(TemplateView):
    """
    The all trials tab of the site
    """
    template_name = 'trials.html'

    def get_context_data(self, **kw):
        """
        Add popular and featured trials to the all trials page
        """
        context = super(AllTrials, self).get_context_data(**kw)
        today = datetime.datetime.today()
        context['active'] = Trial.objects.filter(finish_date__gte=today,
                                                 private=False)
        context['active_featured'] = Trial.objects.filter(finish_date__gte=today,
                                                          featured=True,
                                                          private=False)
        context['past'] = Trial.objects.filter(finish_date__lt=today,
                                               private=False)
        return context


class FeaturedTrialsList(ListView):
    """
    This is the list view for featured Trials - an editorially
    decided subset of all trials.
    """
    queryset            = Trial.objects.filter(featured=True, private=False)
    context_object_name = 'trials'
    template_name       = 'trials/featured_trial_list.html'
