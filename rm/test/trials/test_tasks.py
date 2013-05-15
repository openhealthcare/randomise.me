"""
Unittests for the rm.trials.tasks module
"""
import datetime
import sys
import unittest

from mock import MagicMock, patch

if sys.version_info <  (2, 7): import unittest2 as unittest

from rm import exceptions
from rm.trials import tasks, models

class EmailRmInstructionsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fetches_active(self):
        "Make sure we fetch the active trials"
        mock_trial = MagicMock(name="Mock Rm User Trial")
        with patch.object(models.Trial.objects, 'filter') as ptod:
            ptod.return_value = [mock_trial]
            tasks.email_rm_instructions()
            ptod.assert_called_once_with(instruction_date=datetime.date.today())
            mock_trial.send_instructions.assert_called_once_with()

class InstructLaterTestCase(unittest.TestCase):

    def testSomething(self):
        "Should send participants instructions"
        mock_part = MagicMock(name="Mock Participant")
        with patch.object(models.Participant.objects, 'get') as pget:
            pget.return_value = mock_part
            tasks.instruct_later(3)
            pget.assert_called_once_with(pk=3)
            mock_part.send_instructions.assert_called_once_with()




if __name__ == '__main__':
    unittest.main()
