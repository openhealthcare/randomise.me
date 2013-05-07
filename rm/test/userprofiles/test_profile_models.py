"""
Unittests for the rm.userprofiles.models module
"""
import sys
import unittest

from django.test import utils, TestCase
from mock import MagicMock, patch

if sys.version_info <  (2, 7): import unittest2 as unittest

from rm.userprofiles import models

def setup_module():
    utils.setup_test_environment()

def teardown_module():
    utils.teardown_test_environment()


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



if __name__ == '__main__':
    unittest.main()
