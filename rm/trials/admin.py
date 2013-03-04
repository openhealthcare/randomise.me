"""
Register Trials with the admin site.
"""
from django.contrib import admin

from rm.trials.models import Trial

class TrialAdmin(admin.ModelAdmin):
    """
    Tweak trials in the admin.
    """
    list_filter = ('owner',)
    list_display = ['name', 'url', 'private', 'finish_date', 'owner']

admin.site.register(Trial, TrialAdmin)
