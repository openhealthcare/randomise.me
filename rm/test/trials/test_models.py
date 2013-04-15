"""
Unittests for Randomise.me models
"""
import datetime
import unittest

from rm.trials import models

class SingleUserTrialTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_started(self):
        "Check to see if we can tell a trial has started"
        today = datetime.date.today()
        past = today - datetime.timedelta(days=1)
        future = today + datetime.timedelta(days=1)
        trial = models.SingleUserTrial(start_date=past)
        self.assertEqual(True, trial.started)
        trial = models.SingleUserTrial(start_date=future)
        self.assertEqual(False, trial.started)

    def test_started_no_start_date(self):
        "If there's no start date, we've implicitly not started yet"
        trial = models.SingleUserTrial()
        self.assertEqual(False, trial.started)
