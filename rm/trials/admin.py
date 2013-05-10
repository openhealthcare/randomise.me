"""
Register Trials with the admin site.
"""
from django.contrib import admin

from rm.trials.models import (Trial, Report, Participant, Variable,
                              SingleUserTrial,
                              SingleUserAllocation, SingleUserReport)
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

class ReportAdmin(admin.ModelAdmin):
    """
    Manual admin of data reports
    """
    list_filter = ('trial',)
    list_display = ['trial', 'date', 'group']

class SingleUserTrialAdmin(admin.ModelAdmin):
    """
    Manual admin of SingleUserTrials
    """
    list_display = ['name', 'owner', 'start_date', 'finish_date']

class SingleUserAllocationAdmin(admin.ModelAdmin):
    """
    Manual admin of SingleUserAllocations
    """

class SingleUserReportAdmin(admin.ModelAdmin):
    """
    Manual admin of SingleUserReports
    """
    list_filter = ('trial',)
    list_display = ['trial', 'date', 'group']

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Trial, TrialAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(SingleUserTrial, SingleUserTrialAdmin)
admin.site.register(SingleUserAllocation, SingleUserAllocationAdmin)
admin.site.register(SingleUserReport, SingleUserReportAdmin)
