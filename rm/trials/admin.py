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

admin.site.register(Trial, TrialAdmin)
