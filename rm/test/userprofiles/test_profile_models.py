"""
Unittests for the rm.userprofiles.models module
"""
import sys
import unittest

from django.test import TestCase

from rm.test import rmtestutils
from rm.userprofiles import models

setup_module = rmtestutils.setup_module
teardown_module = rmtestutils.setup_module


class RMUserTestCase(TestCase):

    def test_is_standard(self):
        "Is this user a standard account type?"
        user = models.RMUser()
        self.assertTrue(user.is_standard)

    def test_is_standard_advanced(self):
        user = models.RMUser(account=models.RMUser.ADVANCED)
        self.assertFalse(user.is_standard)

    def test_is_standard_premium(self):
        user = models.RMUser(account=models.RMUser.PREMIUM)
        self.assertFalse(user.is_standard)

    def test_upgrade_standard(self):
        user = models.RMUser()
        user.save()
        self.assertEqual(models.RMUser.STANDARD, user.account)
        user.upgrade()
        self.assertEqual(models.RMUser.ADVANCED, user.account)



if __name__ == '__main__':
    unittest.main()
