"""
Register Trials with the admin site.
"""
from django.contrib import admin

from rm.trials.models import (Trial, Participant, SingleUserTrial,
                              SingleUserAllocation, SingleUserReport)

class TrialAdmin(admin.ModelAdmin):
    """
    Tweak trials in the admin.
    """
    list_filter = ('owner',)
    list_display = ['name', 'url', 'private', 'finish_date', 'owner', 'featured']
    list_editable = ['featured',]

class ParticipantAdmin(admin.ModelAdmin):
    """
    Manual admin of participants
    """

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
admin.site.register(SingleUserTrial, SingleUserTrialAdmin)
admin.site.register(SingleUserAllocation, SingleUserAllocationAdmin)
admin.site.register(SingleUserReport, SingleUserReportAdmin)
