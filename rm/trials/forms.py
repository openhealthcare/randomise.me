"""
Custom forms for the creation of Trials
"""
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
