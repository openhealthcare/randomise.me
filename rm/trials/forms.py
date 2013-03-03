"""
Custom forms for the creation of Trials
"""
#from django import forms
from form_utils.forms import BetterModelForm

from rm.trials.models import Trial

class TrialForm(BetterModelForm):
    """
    Custom user presentation of trials
    """
    class Meta:
        model = Trial
        fieldsets = [
            ('Basic', {'fields': ['name', 'url', 'private'],
                       'legend': 'Basic Details',
                       'description': ''}),
            ('Setup', {'fields': ['question', 'style'],
                       'legend': 'Trial Setup',
                       'classes': ['collapsed']}),
            ('Details', {'fields': ['description', 'group_a', 'group_b',
                                    'instruct_style', 'instruct_hour',
                                    'instruct_date'],
                         'legend': 'Trial Details',
                         'classes': ['collapsed']}),
            ('Sizing', {'fields': ['min_participants', 'max_participants',
                                   'group_a_expected', 'group_b_impressed'],
                        'legend': 'Trial Sizing',
                        'classes': ['collapsed']}),
            ('Duration', {'fields': ['finish_date'],
                          'legend': 'Trial Duration',
                          'classes': ['collapsed']})
            ]
