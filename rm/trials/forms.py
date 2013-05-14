"""
Custom forms for the creation of Trials
"""
import datetime

from django.core.exceptions import ValidationError
from django.forms import fields, widgets
from django.forms.models import inlineformset_factory
from django.forms.models import ModelForm
from django.utils.html import format_html
from form_utils.forms import BetterModelForm

from rm import utils
from rm.trials.models import Trial, Report, Variable, SingleUserTrial, SingleUserReport
from rm.trials import validators

class BootstrapDatepickerWidget(widgets.DateInput):
    """
    Subclass the default date input widget to give us Bootstrap
    friendly datepicker widgets.
    """
    tpl = """<div class="input-append date datepicker" data-date="{today}" data-date-format="dd/mm/yyyy">
    {field} <span class="add-on"><i class="icon-th"></i></span>
</div>"""

    def __init__(self, *args, **kwargs):
        """
        Set the default date value function, then pass up the inheritance tree
        """
        self._default_val = utils.today
        if 'default' in kwargs:
            self._default_val = kwargs.pop('default')
        super(BootstrapDatepickerWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        """
        Take what would be there, add some default attributes, and
        wrap it in a containing div.

        Arguments:
        - `name`:
        - `value`:
        - `attrs`:

        Return:
        Exceptions:
        """
        bs_attrs = dict(
            size="16", type="text", value=self._default_val(), readonly="true"
            )
        attrs.update(bs_attrs)
        markup = super(BootstrapDatepickerWidget, self).render(name, value, attrs)
        return format_html(self.tpl, field=markup, today=utils.today())


class TrialForm(BetterModelForm):
    """
    Custom user presentation of trials
    """
    start_date = fields.DateField(
        input_formats = ['%d/%m/%Y',],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',]))
    finish_date = fields.DateField(
        input_formats = ['%d/%m/%Y', '%Y-%m-%d'],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',],
                                         default=lambda: utils.in_a(week=1)))

    class Meta:
        model = Trial
        fieldsets = [
            ('Basic', {'fields': ['title'],
                       'legend': '1. Hypothesis',
                       'description': ''}),
            ('Details', {'fields': ['participants', 'description',
                                    'group_a_desc', 'group_b_desc'],
                       'legend': '2. Details',
                       'classes': []}),

            ('Instructions', {'fields': ['group_a', 'group_b'],
                         'legend': '3. Instructions',
                         'classes': []}),
            ('Sizing', {'fields': ['min_participants', 'max_participants',
                                   'recruitment'],
                        'legend': '4. Sizing',
                        'classes': []}),
            ('Duration', {'fields': ['start_date', 'finish_date'],
                          'legend': '5. Duration',
                          'classes': []})
            ]

        widgets = {
            'title': widgets.TextInput(attrs={
                    'data-required' : 'true',
                    'data-maxlength': '200'
                    }),
            'style': widgets.Select(attrs={
                    'data-required': 'true'
                    }),
            'description': widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            'group_a': widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            'group_b': widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            'group_a_desc': widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            'group_b_desc': widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            'min_participants': widgets.TextInput(attrs={
                    'data-required': 'true',
                    'data-type'    : 'digits',
                    'data-min'     : '1'
                    }),
            'max_participants': widgets.TextInput(attrs={
                    'data-required': 'true',
                    'data-type'    : 'digits',
                    'data-min'     : '1'
                    }),
            'recruitment': widgets.RadioSelect(),
            }

    def clean_finish_date(self):
        """
        Can we validate that the finish_date isn't in the past please?
        """
        if validators.not_historic(self.cleaned_data['finish_date']):
            return self.cleaned_data['finish_date']


class VariableForm(ModelForm):

    def __init__(self, *args, **kwargs):
        """

        Arguments:
        - `self`:
        - `*args`:
        - `**kwargs`:

        Return:
        Exceptions:
        """
        print 'this'
        ModelForm.__init__(self, *args, **kwargs)


    class Meta:
        model = Variable

        widgets = {
            'style': widgets.Select(attrs={
                    'data-required': 'true'
                    }),
            'question': widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),


            }

# TrialFormSet = inlineformset_factory(TrialForm, Variable)


class TrialReportForm(BetterModelForm):
    """
    Allow the reporting of data for a trial.
    """
    date = fields.DateField(
        input_formats = ['%d/%m/%Y',],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',]))

    class Meta:
        model = Report
        fieldsets = [
            ('Main', {'fields': ['date', 'score'],
                       'legend': 'Report Data',
                       'description': ''}),

            ]

    def clean_date(self):
        """
        Ensure that the date reported on is within the boundaries of
        our trial.

        Ensure that the trial has not been reported on for this date.
        """
        dt = self.cleaned_data['date']
        if validators.during_trial(dt, self.instance.trial.start_date, self.instance.trial.finish_date):
            if validators.no_report(dt, self.instance.trial):
                return dt


class UserTrialForm(BetterModelForm):
    """
    Creating a single user trial for our users
    """
    start_date = fields.DateField(
        input_formats = ['%d/%m/%Y',],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',]))
    finish_date = fields.DateField(
        input_formats = ['%d/%m/%Y',],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',], default=lambda: utils.in_a(week=1)))

    class Meta:
        model = SingleUserTrial
        fieldsets = [
            ('Basic', {'fields': ['name'],
                       'legend': 'Basic Details',
                       'description': ''}),
            ('Setup', {'fields': ['question', 'variable'],
                       'legend': 'Trial Setup',
                       'classes': ['collapsed']}),
            ('Details', {'fields': ['group_a', 'group_b'],
                         'legend': 'Trial Details',
                         'classes': ['collapsed']}),
            ('Duration', {'fields': ['start_date', 'finish_date'],
                          'legend': 'Trial Duration',
                          'classes': ['collapsed']})
            ]
        widgets = {
            'name'      :  widgets.TextInput(attrs={
                    'data-required': 'true',
                    'data-maxlength': '200',
                    'data-trigger':  'focusout change'
                    }),
            'question'  :  widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            'variable'  :  widgets.TextInput(attrs={
                    'Data-required': 'true',
                    'data-maxlength': '200',
                    }),
            'group_a'  :  widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            'group_b'  :  widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            }


class UserReportForm(BetterModelForm):
    """
    Allow the reporting of data for a trial.
    """
    date = fields.DateField(
        input_formats = ['%d/%m/%Y',],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',]))

    class Meta:
        model = SingleUserReport
        fieldsets = [
            ('Main', {'fields': ['date', 'score'],
                       'legend': 'Report Data',
                       'description': ''}),

            ]

    def clean_date(self):
        """
        Ensure that the date reported on is within the boundaries of
        our trial.

        Ensure that the trial has not been reported on for this date.
        """
        dt = self.cleaned_data['date']
        if validators.during_trial(dt, self.instance.trial.start_date, self.instance.trial.finish_date):
            if validators.no_single_report(dt, self.instance.trial):
                return dt
