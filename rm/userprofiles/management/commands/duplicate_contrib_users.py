"""
Convert our user model please
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rm.userprofiles.models import RMUser, BaseUserManager

#User.objects = BaseUserManager()


class Command(BaseCommand):
    """
    Our command.

    Nothing special to see here.
    """
    def handle(self, **options):
        for user in User.objects.all():
            try:
                new_user = RMUser.objects.get(email=user.email)
                print 'found', user, user.email
            except RMUser.DoesNotExist:
                print 'new', user, user.email
                new_user = RMUser()

            new_user.password = user.password
            new_user.is_superuser = user.is_superuser
            new_user.username = user.username
            if user.email:
                new_user.email = user.email
            else:
                new_user.email = '%s@example.com' % user.username
            new_user.is_staff = user.is_staff
            new_user.pk = user.pk


            new_user.save()
