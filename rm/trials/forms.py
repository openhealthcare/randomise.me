"""
Custom forms for the creation of Trials
"""
import datetime


from django.forms import fields, widgets
from django.utils.html import format_html
from form_utils.forms import BetterModelForm

from rm import utils
from rm.trials.models import Trial, SingleUserTrial, SingleUserReport
from rm.trials.validators import not_historic

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
    finish_date = fields.DateField(
        input_formats = ['%d/%m/%Y', '%Y-%m-%d'],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',],
                                         default=lambda: utils.in_a(week=1)))

    class Meta:
        model = Trial
        fieldsets = [
            ('Basic', {'fields': ['name', 'url', 'private'],
                       'legend': 'Basic Details',
                       'description': ''}),
            ('Setup', {'fields': ['description', 'style'],
                       'legend': 'Trial Setup',
                       'classes': ['collapsed']}),
            ('Details', {'fields': ['group_a', 'group_b'],
                         'legend': 'Trial Details',
                         'classes': ['collapsed']}),
            ('Sizing', {'fields': ['min_participants', 'max_participants'],
                        'legend': 'Trial Sizing',
                        'classes': ['collapsed']}),
            ('Duration', {'fields': ['finish_date'],
                          'legend': 'Trial Duration',
                          'classes': ['collapsed']})
            ]

    def clean_finish_date(self):
        """
        Can we validate that the finish_date isn't in the past please?
        """
        if not_historic(self.cleaned_data['finish_date']):
            return self.cleaned_data['finish_date']


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
                    'data-required': 'true',
                    'data-maxlength': '200',
                    }),
            'group_a'  :  widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            'group_b'  :  widgets.Textarea(attrs={
                    'data-required': 'true'
                    }),
            }

    # def clean_finish_date(self):
    #     """
    #     Can we validate that the finish_date isn't in the past please?
    #     """
    #     not_historic(self.cleaned_data['finish_date'])

    # def clean_start_date(self):
    #     """
    #     Can we validate that the start_date isn't in the past please?
    #     """
    #     not_historic(self.cleaned_data['start_date'])

class UserReportForm(BetterModelForm):
    """
    Allow the reporting of data for a trial.
    """
    class Meta:
        model = SingleUserReport
        fieldsets = [
            ('Main', {'fields': ['date', 'score'],
                       'legend': 'Report Data',
                       'description': ''}),

            ]
