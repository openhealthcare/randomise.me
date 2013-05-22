"""
Register Trials with the admin site.
"""
from django.contrib import admin

from rm.trials.models import (Trial, Report, Participant, Variable)

class VariableInline(admin.StackedInline):
    model = Variable

class TrialAdmin(admin.ModelAdmin):
    """
    Tweak trials in the admin.
    """
    list_filter = ('owner',)
    list_display = ['title', 'private', 'finish_date', 'owner', 'featured']
    list_editable = ['featured',]
    inlines = [VariableInline]

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
    list_display = ['trial', 'date', 'group']

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Trial, TrialAdmin)
admin.site.register(Report, ReportAdmin)
