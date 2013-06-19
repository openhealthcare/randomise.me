"""
Custom forms for the creation of Trials
"""
import datetime

from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields, widgets
from django.forms.models import inlineformset_factory
from django.forms.models import ModelForm
from django.utils.html import format_html
from form_utils.forms import BetterModelForm

from rm import utils
from rm.trials.models import Trial, Report, Variable
from rm.trials import validators
from rm.userprofiles.models import RMUser

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




class TrialForm(ModelForm):
    """
    Custom user presentation of trials
    """
    reporting_date = fields.DateField(
        input_formats = ['%d/%m/%Y', '%Y-%m-%d'],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',],
                                         default=lambda: utils.today()))

    instruction_date = fields.DateField(
        input_formats = ['%d/%m/%Y', '%Y-%m-%d'],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',],
                                         default=lambda: utils.today()))
    ending_date = fields.DateField(
        input_formats = ['%d/%m/%Y', '%Y-%m-%d'],
        widget=BootstrapDatepickerWidget(format=['%d/%m/%Y',],
                                         default=lambda: utils.today()))

    class Meta:
        model = Trial
        exclude = ['owner', 'created', 'recruitment']
        widgets = {
            'title': widgets.TextInput(attrs={
                    'class': 'wider',
                    'data-required' : 'true',
                    'data-maxlength': '200'
                    }),
            'reporting_freq': widgets.Select(
                attrs={
                    'data-required': 'true'
                    }),
            'reporting_style': widgets.RadioSelect(attrs={
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
            'ending_style': widgets.RadioSelect(),
            'ending_reports': widgets.TextInput(attrs={
                    'data-type': 'digits',
                    'data-min' : '1'
                    }),
            }



class N1TrialForm(ModelForm):
    """
    Setup for N1 trial specifics.
    """
    ending_reports = fields.IntegerField(
        label="Number of observations",
        widget=widgets.TextInput(attrs={
                'data-type': 'digits',
                'data-min' : '1'
                }))

    class Meta:
        model = Trial
        exclude = ['owner', 'created']
        widgets = {
            'title': widgets.TextInput(attrs={
                    'class': 'wider',
                    'data-required' : 'true',
                    'data-maxlength': '200'
                    }),
            'instruction_delivery': widgets.HiddenInput(),
            'ending_style': widgets.HiddenInput(),
            }

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


class TutorialForm(forms.Form):
    """
    The form we use to create v.simple trials from the get started page
    """
    title = forms.CharField(max_length=100,
                            widget=widgets.TextInput(attrs={
                'class': 'wider',
                'placeholder': "What's your question?",
                'data-required' : 'true',
                'data-maxlength': '200'
                }))

    measure_style = forms.ChoiceField(choices=Variable.STYLE_CHOICES,
                                      widget=widgets.Select(attrs={
                'data-required': 'true',
                }),
                                      initial=Variable.SCORE)

    measure_question = forms.CharField(widget=widgets.Textarea(attrs={
                'data-required': 'true',
                'class': 'wider',
                'placeholder': 'What is the question that lets you measure your outcome?'
                }))

    group_a = forms.CharField(widget=widgets.Textarea(attrs={
                'data-required': 'true',
                'class': 'wider',
                'placeholder': 'Group A instructions'
                }))

    group_b = forms.CharField(widget=widgets.Textarea(attrs={
                    'data-required': 'true',
                    'class': 'wider',
                    'placeholder': 'Group B instructions'
                    }))

    email = forms.EmailField(widget=widgets.TextInput(attrs={
                'data-required': 'true',
                'data-type': 'email',
                'placeholder': 'email'
                }),
                             required=False)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
                'data-required': 'true',
                'id': 'password1',
                'placeholder': 'password',
                }),
                               required=False)
    password_confirmation = forms.CharField(max_length=200,
                                            widget=forms.PasswordInput(attrs={
                'data-required': 'true',
                'data-equalto': '#password1',
                'placeholder': 'password confirmation',
                }),
                                            required=False)

    def __init__(self, *args, **kw):
        self.user = None
        self.request = kw['request']
        del kw['request']
        super(TutorialForm, self).__init__(*args, **kw)

    def clean(self):
        """"
        Check that the credentials supplied are valid:

        * If the user is logged in, just bail - we're cool.
        * If the email is new to us, that's cool, we'll sign 'em up
        * If the email is known and the password is correct, we'll log 'em in
        * If the email is taken and the password is wrong, we'll add an error
        * We rely on Parsley.js to make sure the password && confirmation are accurate
        """
        cleaned_data = super(TutorialForm, self).clean()
        if self.request.user.is_authenticated():
            return cleaned_data
        email, password = cleaned_data['email'], cleaned_data['password']
        if RMUser.objects.filter(email=email).count() > 0:
            user = RMUser.objects.get(email=email)
            if not user.check_password(password):
                # Manually ovveride dependant fields with errors here.
                # see https://docs.djangoproject.com/en/dev/ref/forms/validation/\
                # #cleaning-and-validating-fields-that-depend-on-each-other
                msg = u"This email address has already been used for a Randomise Me account, and the password didn't match the one we have associated with it - check your typing and try again"
                self._errors['password'] = self.error_class([msg])

                # need to take these out for downstream processing
                del cleaned_data['password']
                del cleaned_data['password_confirmation']
            else:
                self.user = user

        return cleaned_data
