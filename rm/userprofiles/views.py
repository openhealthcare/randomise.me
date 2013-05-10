"""
Views that allow us to edit user profile data
"""
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView

from rm.userprofiles.forms import ProfileForm
from rm.userprofiles.models import RMUser


class RMUserUpdate(UpdateView):
    model      = RMUser
    form_class = ProfileForm
    success_url = reverse_lazy('account-edit')

    def get_object(self, *args, **kwargs):
        """
        Override the default get object to return the currently
        logged in user.
        """
        return self.request.user
