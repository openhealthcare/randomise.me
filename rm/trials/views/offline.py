"""
Views related to offline trials.
"""
import re

from django.http import HttpResponseRedirect
from django.views.generic import View, FormView
import ffs
from ffs.formats import CSV

from rm.http import LoginRequiredMixin, JsonResponse, serve_maybe
from rm.trials.forms import (OfflineTrialForm, OfflineParticipantsForm,
                             OfflineResultsForm)
from rm.trials.models import Trial, Variable, Participant, Report
from rm.trials.views import TrialByPkMixin, OwnsTrialMixin

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
        trial = Trial(
            owner=self.request.user,
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            group_a=form.cleaned_data['group_a'],
            group_b=form.cleaned_data['group_b'],
            offline=True,
            min_participants=100
            )
        trial.save()

        variable = Variable(
            trial=trial,
            name=form.cleaned_data['measure_name'],
            style=form.cleaned_data['measure_style']
            )
        variable.save()

        return HttpResponseRedirect(trial.get_absolute_url())


class UploadOfflineParticipantsView(TrialByPkMixin, OwnsTrialMixin, FormView):
    """
    Handle CSV uploads of offline trial participants
    """
    form_class = OfflineParticipantsForm

    def form_invalid(self, form):
        """
        Handle a badly constructed request.
        """
        if form.errors.get('participants') == ['This field is required.']:
            return JsonResponse('Must upload a file!', status=401)
        return JsonResponse(form.errors, status=401)

    def form_valid(self, form):
        """
        Handle the uploaded participants.
        """
        participant_list = [l.strip()
                            for l in
                            form.cleaned_data['participants'].readlines()]
        if not all(re.match(r'^[a-zA-Z0-9_]+$', part)
                   for part in participant_list):
            return JsonResponse('Your participant identifiers are not ^[a-zA-Z0-9_]+$', status=401)

        for part in participant_list:
            participant = Participant(identifier=part, trial=self.trial)
            participant.randomise()

        return JsonResponse(True)


class UploadOfflineResultsView(TrialByPkMixin, OwnsTrialMixin, FormView):
    """
    Handle CSV uploads of offline trial results
    """
    form_class = OfflineResultsForm

    def form_invalid(self, form):
        """
        Handle a badly constructed request.
        """
        if form.errors.get('results') == ['This field is required.']:
            return JsonResponse('Must upload a file!', status=401)
        return JsonResponse(form.errors, status=401)

    def form_valid(self, form):
        """
        Handle the uploaded results.
        """
        csv = [r.strip().split(',')
               for r in form.cleaned_data['results'].readlines()]
        try:
            for identifier, group, result in csv:
                try:
                    participant = Participant.objects.get(
                        identifier=identifier,
                        trial=self.trial
                        )
                    variable = self.trial.variable_set.get()
                    report = Report(trial=self.trial,
                                    participant=participant,
                                    variable=variable,
                                    group=participant.group)
                    if variable.style == Variable.SCORE:
                        report.score = int(result)
                    elif variable.style == Variable.COUNT:
                        report.score = float(count)
                    elif variable.style == Variable.BINARY:
                        report.binary = bool(result)

                    report.save()

                except Participant.DoesNotExist:
                    return JsonResponse('No participant {0}'.format(identifier),
                                        status=401)
                except Exception as err:
                    raise
        except ValueError:
            err = "We couldn't find an identifier, group and result for every row :("
            return JsonResponse(err, status=401)

        self.trial.stop()
        return JsonResponse(True)


class DownloadOfflineParticipantsView(TrialByPkMixin, OwnsTrialMixin, View):
    """
    Download the csv of participants
    """

    @serve_maybe
    def get(self, request, pk):
        """
        Serve a CSV of this trial's grouped participants
        """
        rows = [
            (participant.identifier, participant.group)
            for participant in self.trial.participant_set.all()
            ]

        raw = ffs.Path.newfile()
        with raw.csv() as csv:
            csv.writerows(rows)
        return raw
