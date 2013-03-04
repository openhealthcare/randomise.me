"""
Register Trials with the admin site.
"""
from django.contrib import admin

from rm.trials.models import Trial, Participant

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

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Trial, TrialAdmin)
