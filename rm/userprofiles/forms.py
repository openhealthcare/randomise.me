"""
Custom forms for user profile data
"""
from django.forms import fields, widgets, ModelForm

from rm.userprofiles.models import RMUser

class ProfileForm(ModelForm):
    """
    Custom form for editing our user profile.
    """
    class Meta:
        model = RMUser
        fields = ['name', 'email', 'receive_questions', 'dob', 'gender', 'postcode']
        widgets = {
            'gender': widgets.RadioSelect()
            }
