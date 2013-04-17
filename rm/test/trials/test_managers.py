"""
Unittests for the trial managers
"""
import datetime
import unittest

from mock import patch

from rm.trials import managers

class TemporalTestCase(unittest.TestCase):
    def setUp(self):
        super(TemporalTestCase, self).setUp()
        self.today = datetime.date.today()

class SingleUserTrialManagerTestCase(TemporalTestCase):

    def test_active(self):
        "Return the currently active models"
        manager = managers.SingleUserTrialManager()
        with patch.object(manager, 'filter') as pfilt:
            manager.active()
            pfilt.assert_called_once_with(start_date__lte=self.today,
                                          finish_date__gte=self.today)

    def test_starting_today(self):
        "Return trials that start today"
        manager = managers.SingleUserTrialManager()
        with patch.object(manager, 'filter') as pfilt:
            manager.starting_today()
            pfilt.assert_called_once_with(start_date=self.today)


class RmTrialManagerTestCase(TemporalTestCase):

    def test_active(self):
        "Return the currently active models"
        manager = managers.RmTrialManager()
        with patch.object(manager, 'filter') as pfilt:
            manager.active()
            pfilt.assert_called_once_with(start_date__lte=self.today,
                                          finish_date__gte=self.today)

    def test_starting_today(self):
        "Return trials that start today"
        manager = managers.RmTrialManager()
        with patch.object(manager, 'filter') as pfilt:
            manager.starting_today()
            pfilt.assert_called_once_with(start_date=self.today)
