"""
Unittests for the rm.trials.tasks module
"""
import sys
import unittest

from mock import MagicMock, patch

if sys.version_info <  (2, 7): import unittest2 as unittest

from rm.trials import tasks

class EmailSingleInstructionsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fetches_active(self):
        "Make sure we fetch the active trials"
        mock_trial = MagicMock(name="Mock Single User Trial")
        with patch.object(tasks.models.SingleUserTrial.objects, 'active') as pact:
            pact.return_value = [mock_trial]
            tasks.email_single_instructions()
            pact.assert_called_once_with()
            mock_trial.send_instructions.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
