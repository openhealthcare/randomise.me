"""
Unittests for the trial managers
"""
import datetime
import unittest

from mock import MagicMock, patch

from rm.trials import managers
from rm.trials.models import Trial

class RmTrialManagerTestCase(unittest.TestCase):

    def setUp(self):
        super(RmTrialManagerTestCase, self).setUp()
        self.today = datetime.date.today()
        self.manager = managers.RmTrialManager()

    def test_completed(self):
        "Get stopped"
        with patch.object(self.manager, 'filter') as pfilt:
            self.manager.completed()
            pfilt.assert_called_once_with(stopped=True)

    def test_recruiting(self):
        "Get recruiting trials"
        with patch.object(self.manager, 'filter') as pfilt:
            self.manager.recruiting()
            pfilt.assert_called_once_with(private=False, stopped=False,
                                          n1trial=False, recruitment=Trial.ANYONE)

    def test_ending_today(self):
        "Get ends"
        with patch.object(self.manager, 'filter') as pfilt:
            self.manager.ending_today()
            pfilt.assert_called_once_with(ending_style=Trial.DATED,
                                          ending_date=datetime.date.today())

    def test_reproduce(self):
        "Kill non-reproduced fields"
        mock_user = MagicMock(name='Mock User')
        with patch.object(self.manager, 'get') as pget:
            new = self.manager.reproduce(mock_user, pk=1)
            pget.assert_called_once_with(pk=1)
            self.assertEqual(new.pk, None)
            self.assertEqual(new.instruction_date, None)
            self.assertEqual(new.featured, None)
