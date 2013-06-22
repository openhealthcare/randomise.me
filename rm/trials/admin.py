"""
Register Trials with the admin site.
"""
from django.contrib import admin

from rm.trials.models import (Trial, Report, Participant, Variable, TutorialExample)

class VariableInline(admin.StackedInline):
    model = Variable

class TrialAdmin(admin.ModelAdmin):
    """
    Tweak trials in the admin.
    """
    list_filter = ('owner__email', 'n1trial', 'private')
    list_display = ['title', 'pk', 'private', 'owner', 'featured', 'n1trial', 'stopped',
                    'recruitment']
    list_search = ['title', 'description', 'group_a', 'group_b']
    list_editable = ['featured',]
    inlines = [VariableInline]

class VariableAdmin(admin.ModelAdmin):
    list_display = ('trial', 'question', 'style')
    list_filter = ['trial', 'style']

class ParticipantAdmin(admin.ModelAdmin):
    """
    Manual admin of participants
    """
    list_filter = ('user', 'trial')

class ReportAdmin(admin.ModelAdmin):
    """
    Manual admin of data reports
    """
    list_filter = ('trial',)
    list_display = ['trial', 'date', 'group', 'get_value']

class TutorialAdmin(admin.ModelAdmin):
    list_display  = ['name', 'question', 'measure_style', 'measure_question', 'group_a', 'group_b']
    list_editable = ['question', 'measure_style', 'measure_question', 'group_a', 'group_b']

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Trial, TrialAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(TutorialExample, TutorialAdmin)
