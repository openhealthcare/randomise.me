"""
Unittests for Form validators
"""
import datetime
import unittest

from django.core.exceptions import ValidationError
from mock import MagicMock

from rm.trials import validators

class NotHistoricTestCase(unittest.TestCase):

    def test_returns_true(self):
        "should return True"
        future = datetime.date.today() + datetime.timedelta(days=1)
        resp = validators.not_historic(future)
        self.assertEqual(True, resp)


class DuringTrialTestCase(unittest.TestCase):
    def setUp(self):
        self.trial = MagicMock(name='Mock Trial')
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.tomorrow = self.today + datetime.timedelta(days=1)

    def test_on_start_date(self):
        "True"
        self.assertEqual(True, validators.during_trial(self.today, self.today, self.tomorrow))

    def test_on_finish_date(self):
        "True"
        self.assertEqual(True, validators.during_trial(self.today, self.yesterday, self.today))

    def test_during_trial(self):
        "True"
        self.assertEqual(True, validators.during_trial(self.today, self.yesterday, self.tomorrow))

    def test_before_start(self):
        "Should Raise"
        with self.assertRaises(ValidationError):
            validators.during_trial(self.today, self.tomorrow, self.tomorrow)

    def test_after_finish(self):
        "Should Raise"
        with self.assertRaises(ValidationError):
            validators.during_trial(self.today, self.yesterday, self.yesterday)
