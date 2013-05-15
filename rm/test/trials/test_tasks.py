"""
Unittests for the rm.trials.tasks module
"""
import datetime
import sys
import unittest

from mock import MagicMock, patch

if sys.version_info <  (2, 7): import unittest2 as unittest

from rm import exceptions
from rm.trials import tasks

class EmailRmInstructionsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fetches_active(self):
        "Make sure we fetch the active trials"
        mock_trial = MagicMock(name="Mock Rm User Trial")
        with patch.object(tasks.models.Trial.objects, 'filter') as ptod:
            ptod.return_value = [mock_trial]
            tasks.email_rm_instructions()
            ptod.assert_called_once_with(instruction_date=datetime.date.today())
            mock_trial.send_instructions.assert_called_once_with()



if __name__ == '__main__':
    unittest.main()
