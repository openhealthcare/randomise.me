"""
Unittests for the trial managers
"""
import datetime
import unittest

from mock import patch

from rm.trials import managers

class SingleUserTrialManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.today = datetime.date.today()

    def test_active(self):
        "Return the currently active models"
        manager = managers.SingleUserTrialManager()
        with patch.object(manager, 'filter') as pfilt:
            manager.active()
            pfilt.assert_called_once_with(start_date__lte=self.today,
                                          finish_date__gte=self.today)
