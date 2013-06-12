"""
Superuser login
"""
from django.contrib.auth import login, authenticate

from rm.userprofiles.models import RMUser as User

# So I can invoked authenticate recursively below
django_authenticate = authenticate

class SuperuserLoginAuthenticationBackend(object):
    """ Let superusers login as regular users. """
    def authenticate(self, username=None, password=None, email=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        # The password should be name/password
        if "@" not in password:
            return None
        supername, superpass = password.split(":", 1)
        superuser = django_authenticate(email=supername, password=superpass)
        if superuser and superuser.is_superuser:
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
