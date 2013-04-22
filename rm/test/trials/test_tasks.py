"""
Unittests for the rm.trials.tasks module
"""
import sys
import unittest

from mock import MagicMock, patch

if sys.version_info <  (2, 7): import unittest2 as unittest

from rm import exceptions
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

    def test_no_email(self):
        "If a user has no email, continue."
        def raiser():
            raise exceptions.NoEmailError()

        mock_trial1 = MagicMock(name="Mock Single User Trial 1")
        mock_trial1.send_instructions.side_effect = raiser
        mock_trial2 = MagicMock(name="Mock Single User Trial 2")
        with patch.object(tasks.models.SingleUserTrial.objects, 'active') as pact:
            pact.return_value = [mock_trial1, mock_trial2]
            tasks.email_single_instructions()
            mock_trial2.send_instructions.assert_called_once_with()


class EmailRmInstructionsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fetches_active(self):
        "Make sure we fetch the active trials"
        mock_trial = MagicMock(name="Mock Rm User Trial")
        with patch.object(tasks.models.Trial.objects, 'starting_today') as ptod:
            ptod.return_value = [mock_trial]
            tasks.email_rm_instructions()
            ptod.assert_called_once_with()
            mock_trial.randomise.assert_called_once_with()
            mock_trial.send_instructions.assert_called_once_with()



if __name__ == '__main__':
    unittest.main()
