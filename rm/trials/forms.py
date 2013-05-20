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
from rm.trials.models import Trial, Report, Variable
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
        self.format = '%d/%m/%Y'

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
        widget=BootstrapDatepickerWidget(
            format=['%d/%m/%Y',],
            attrs={
                'data-rmafterdate':"#id_start_date",
                'data-rmafterdate-message': "Finish date can't be after the start date"
                },
            default=lambda: utils.in_a(week=1)))
    instruction_date = fields.DateField(
        input_formats = ['%d/%m/%Y', '%Y-%m-%d'],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',],
                                         default=lambda: utils.today()))

    class Meta:
        model = Trial
        fieldsets = [
            ('Basic', {'fields': ['title', 'reporting_freq'],
                       'legend': '1. Hypothesis',
                       'description': ''}),
            ('Details', {'fields': ['participants', 'description',
                                    'group_a_desc', 'group_b_desc'],
                       'legend': '2. Details',
                       'classes': []}),

            ('Instructions', {'fields': ['group_a', 'group_b', 'instruction_delivery',
                                         'instruction_hours_after', 'instruction_date'],
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
            'reporting_freq': widgets.Select(
                attrs={
                    'data-required': 'true'
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
            'instruction_delivery': widgets.RadioSelect(),
            'instruction_hours_after': widgets.TextInput(attrs={
                    'data-type'    : 'digits',
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
                    'data-min'     : '1',
                    'data-greaterthanorequalto': "#id_min_participants",
                    'data-greaterthanorequalto-message': "Max participants must be greater than or equal to Min participants"
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


class BaseTrialReportForm(ModelForm):
    """
    Allow the reporting of data for a trial.
    """
    date = fields.DateField(
        input_formats = ['%d/%m/%Y',],
        widget=BootstrapDatepickerWidget(
            format=['%d/%m/%Y',],
            ))

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


class ScoreReportForm(BaseTrialReportForm):
    """
    Report on a score 1-10 variable
    """
    SCORE_CHOICES = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8),
        (9,9),
        (10,10)
        )

    class Meta:
        score = True
        model = Report

    score = fields.IntegerField(
        widget=widgets.Select(choices=SCORE_CHOICES, attrs={
                'data-required': 'true'
                })
        )


class BinaryReportForm(BaseTrialReportForm):
    """
    Report on a binary outcome
    """
    class Meta:
        binary = True
        model = Report

    binary = fields.NullBooleanField(
        widget= widgets.NullBooleanSelect(attrs={
                'data-required': 'true'
                }))


class CountReportForm(BaseTrialReportForm):
    """
    Report on count outcome
    """
    class Meta:
        count = True
        model = Report

    count = fields.IntegerField(
        widget=widgets.TextInput(attrs={
                'data-required': 'true',
                'data-type': 'digits'
                }))



def reportform_factory(variable, initial):
    """
    Return a reportform that has the correct inputs.


    Arguments:
    - `variable`: Variable
    - `initial`: dict

    Return: Form
    Exceptions: None
    """
    if variable.style == variable.SCORE:
        return ScoreReportForm(initial=initial)
    elif variable.style == variable.BINARY:
        return BinaryReportForm(initial=initial)
    elif variable.style == variable.COUNT:
        return CountReportForm()
    raise ValueError('No variable style - what the what?')
