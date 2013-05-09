"""
A create trial view?
"""
import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, View, ListView
from django.views.generic.edit import CreateView, BaseCreateView
from django.utils import simplejson
from extra_views import CreateWithInlinesView, InlineFormSet
from extra_views import NamedFormsetsMixin, ModelFormSetView
import ffs

from rm import exceptions
from rm.trials.forms import (TrialForm, TrialReportForm, UserTrialForm,
                             UserReportForm)
from rm.trials.models import Trial, Report, Variable, SingleUserTrial, SingleUserReport

def serve_maybe(meth):
    """
    Decorator to figure out if we want to serve files
    ourselves (DEBUG) or hand off to Nginx
    """
    # Originally from Open Prescribing raw.views

    def handoff(self, *args, **kwargs):
        """
        Internal wrapper function to figure out
        the logic
        """
        filename = meth(self, *args, **kwargs)

        # When we're running locally, just take the hit, otherwise
        # offload the serving of the datafile to Nginx
        if settings.DEBUG:
            resp = HttpResponse(
                open(filename, 'rb').read(),
                mimetype='application/force-download'
                )
            return resp

        resp = HttpResponse()
        url = '/protected/{0}'.format(filename)
        # let nginx determine the correct content type
        resp['Content-Type']=""
        resp['X-Accel-Redirect'] = url
        return resp

    return handoff


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
        print self.trial
        return super(ReportView, self).get(*args, **kw)

    def post(self, *args,**kw):
        """
        Store the trial isntance
        """

        self.trial = self.trial_model.objects.get(pk=kw['pk'])
        date = datetime.datetime.strptime(self.request.POST['date'], '%d/%m/%Y').date()
        group = self.trial.participant_set.get(user=self.request.user).group

        for variable in self.trial.variable_set.all():
            report = Report.objects.get_or_create(trial=self.trial, date=date,
                                                  group=group, variable=variable)[0]
            report.score = int(self.request.POST['id-'+variable.name])
            report.save()

        return HttpResponseRedirect(self.trial.get_absolute_url())

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


class TrialReport(ReportView):
    """
    Report a data point for this trial
    """
    model       = Report
    trial_model = Trial


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

    def get_context_data(self, **kw):
        """
        Determine the detail template appropriate for this user

        Return: dict
        Exceptions: None
        """
        context = super(TrialDetail, self).get_context_data(**kw)
        trial = context['trial']
        detail_template = 'trials/trial_detail_recruiting.html'
        if trial.finished:
            detail_template = 'trials/trial_detail_report.html'

        if self.request.user.is_authenticated():
            if trial.owner == self.request.user:
                detail_template = 'trials/trial_detail_owner.html'
            elif trial.participant_set.filter(user=self.request.user).count() > 0:
                detail_template = 'trials/trial_detail_participant.html'

        context['detail_template'] = detail_template
        return context


class VariableInline(InlineFormSet):
    model = Variable

class TrialCreate(NamedFormsetsMixin, CreateWithInlinesView):
    model = Trial
    context_object_name = "trial"
    model               = Trial
    form_class          = TrialForm
    inlines = [VariableInline]
    inlines_names = ['Variable']

    def get_form(self, klass):
        """
        Add ownership details to the trial
        """
        form = super(TrialCreate, self).get_form(klass)
        form.instance.owner = self.request.user
        return form

class ReproduceTrial(LoginRequiredMixin, CreateView):
    """
    Forkin' action.
    """
    context_object_name = "trial"
    model               = Trial
    form_class          = TrialForm

    def get_template_names(self, *args, **kwargs):
        return ['trials/reproduce_trial.html']

    def get(self, request, *args, **kwargs):
        """
        If the self.object we get from our parent classes is None
        then fill it out with the object we're copying.

        Arguments:
        - `request`: Request

        Return: Response
        Exceptions:
        """
        self.object = Trial.objects.reproduce(request.user, pk=kwargs['pk'])
        print self.object
        return super(BaseCreateView, self).get(request, *args, **kwargs)


    def form_valid(self, form):
        """
        Add ownership details to the trial
        """
        form.instance.owner = self.request.user
        return super(ReproduceTrial, self).form_valid(form)


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

class TrialAsCsv(View):
    """
    Download the trial's raw data as a csv.
    """

    @serve_maybe
    def get(self, request, pk):
        """
        We want to serve a CSV of this trial's raw data!

        Return: str
        Exceptions: None
        """
        trial = Trial.objects.get(pk=pk)
        rows = [
            (report.group.name, report.date.isoformat(), report.score)
            for report in trial.report_set.all()
            ]

        raw = ffs.Path.newfile()
        with raw.csv() as csv:
            csv.writerows([[
                    'group',
                    'date'
                    'score'
                    ]] + rows)
        return raw


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
