"""
Unittests for Randomise.me models
"""
import datetime
import unittest

from django.core import mail
from django.test import utils, TestCase
from mock import MagicMock, patch

from rm import exceptions
from rm.trials import models

def setup_module():
    utils.setup_test_environment()

def teardown_module():
    utils.teardown_test_environment()


class TemporalTestCase(TestCase):
    def setUp(self):
        super(TemporalTestCase, self).setUp()
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.tomorrow = self.today + datetime.timedelta(days=1)


class TrialTestCase(TemporalTestCase):

    def test_time_remaining(self):
        "How much remaining time is there?"
        trial = models.Trial(finish_date=self.tomorrow)
        self.assertEqual(datetime.timedelta(days=1), trial.time_remaining())

    def test_time_remaining_finished(self):
        "Finished string"
        trial = models.Trial(finish_date=self.yesterday)
        self.assertEqual('Trial finished', trial.time_remaining())

    def test_can_join_finished(self):
        "Can't join a finished trial"
        trial = models.Trial(finish_date=self.yesterday)
        self.assertEqual(False, trial.can_join())

    def can_join_open(self):
        "Can join an open trial"
        trial = models.Trial(finish_date=self.tomorrow, max_participants=2)
        with patch.object(trial.participant_set, 'count') as pcount:
            pcount.return_value = 1
            self.assertEqual(True, trial.can_join())

    def can_join_full(self):
        "Can join an open trial"
        trial = models.Trial(finish_date=self.tomorrow, max_participants=2)
        with patch.object(trial.participant_set, 'count') as pcount:
            pcount.return_value = 2
            self.assertEqual(False, trial.can_join())


class SingleUserTrialTestCase(TemporalTestCase):

    def setUp(self):
        super(SingleUserTrialTestCase, self).setUp()
        self.user = models.User(email='larry@example.com')

    def tearDown(self):
        super(SingleUserTrialTestCase, self).tearDown()
        mail.outbox = []

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

    def test_email_instructions_no_to_email(self):
        "Should raise"
        trial = models.SingleUserTrial(owner=models.User())
        with self.assertRaises(exceptions.NoEmailError):
            trial._email_instructions('Do it', self.today)

    def test_email_instructions_subject(self):
        "Should send email"
        trial = models.SingleUserTrial(name="This", owner=self.user, pk=1)
        trial._email_instructions('Do it', datetime.date(1984, 12, 22))
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(
            'Randomise.me - instructions for This 22/12/1984',
            mail.outbox[0].subject)

    def test_email_instructions_body(self):
        "Should include instructions"
        trial = models.SingleUserTrial(owner=self.user, pk=1)
        trial._email_instructions('Do it', datetime.date(1984, 12, 22))
        self.assertEqual(1, len(mail.outbox))
        for content in [mail.outbox[0].body, mail.outbox[0].alternatives[0][0]]:
            self.assertNotEqual(-1, content.find('Do it'))
            self.assertNotEqual(-1, content.find('22/12/1984'))

    def test_email_instructions_from(self):
        "Should be from email"
        trial = models.SingleUserTrial(owner=self.user, pk=1)
        with self.settings(DEFAULT_FROM_EMAIL='from@example.com'):
            trial._email_instructions('Do it', datetime.date(1984, 12, 22))
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual('from@example.com', mail.outbox[0].from_email)

    def test_email_instructions_to(self):
        "Should be the owner's email"
        user = models.User(email = 'larry@example.com')
        trial = models.SingleUserTrial(owner=user, pk=1)
        trial._email_instructions('Do it', datetime.datetime(1984, 12, 22))
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(['larry@example.com'], mail.outbox[0].to)

    def test_send_instructions(self):
        "Should send instructions to our owner"
        trial = models.SingleUserTrial(
            start_date=self.yesterday,
            finish_date=self.tomorrow,
            )
        with patch.object(models.SingleUserTrial, '_email_instructions') as pemail:
            with patch.object(models.SingleUserTrial, 'instructions_on') as pinst:
                pinst.return_value = 'Foo a'
                trial.send_instructions()
                pemail.assert_called_once_with('Foo a', self.today)

    def test_send_instructions_finished(self):
        "Should raise"
        trial = models.SingleUserTrial(finish_date=self.yesterday)
        with self.assertRaises(exceptions.TrialFinishedError):
            trial.send_instructions()

    def test_send_instructions_not_started(self):
        "Should raise"
        trial = models.SingleUserTrial(start_date=self.tomorrow)
        with self.assertRaises(exceptions.TrialNotStartedError):
            trial.send_instructions()

    def test_instructions_on(self):
        "Get the instructions for a particular day"
        trial = models.SingleUserTrial(finish_date=self.tomorrow)
        with patch.object(models.SingleUserAllocation, 'instructions_on') as pfor:
            pfor.return_value = 'foo bar'
            instructions = trial.instructions_on(self.today)
            self.assertEqual('foo bar', instructions)
            pfor.assert_called_once_with(trial, self.today)

    def test_instructions_on_too_early(self):
        "Should raise"
        trial = models.SingleUserTrial(start_date=self.tomorrow)
        with self.assertRaises(exceptions.TrialNotStartedError):
            trial.instructions_on(self.today)

    def test_instructions_on_too_late(self):
        "Should raise"
        trial = models.SingleUserTrial(finish_date=self.yesterday)
        with self.assertRaises(exceptions.TrialFinishedError):
            trial.instructions_on(self.today)


class SingleUserAllocationTestCase(TemporalTestCase):

    def setUp(self):
        super(SingleUserAllocationTestCase, self).setUp()
        self.trial = models.SingleUserTrial(
            start_date=self.yesterday,
            finish_date=self.tomorrow,
            group_a='Foo a',
            group_b='Foo b'
            )

    def test_instructions_on(self):
        "Allocate"
        mock_allocation = MagicMock(name='Mock Single User Allocation')
        mock_allocation.group = 'A'
        with patch.object(models.SingleUserAllocation.objects, 'get_or_create') as pget:
            pget.return_value = [mock_allocation]

            instructions = models.SingleUserAllocation.instructions_on(self.trial, self.today)
            self.assertEqual('Foo a', instructions)
            pget.assert_called_once_with(trial=self.trial, date=self.today)

    def test_instructions_on_create(self):
        "Allocate"
        mock_allocation = MagicMock(name='Mock Single User Allocation')
        mock_allocation.group = None
        def randomise():
            mock_allocation.group = 'A'

        mock_allocation.randomise.side_effect = randomise

        with patch.object(models.SingleUserAllocation.objects, 'get_or_create') as pget:
            pget.return_value = [mock_allocation]

            instructions = models.SingleUserAllocation.instructions_on(self.trial, self.today)
            self.assertEqual('Foo a', instructions)
            pget.assert_called_once_with(trial=self.trial, date=self.today)
            mock_allocation.randomise.assert_called_once_with()
            mock_allocation.save.assert_called_once_with()

    def test_randomise(self):
        "Allocate the instance."
        allocation = models.SingleUserAllocation()
        with patch.object(models.random, 'choice') as pchoice:
            pchoice.return_value = 'A'
            allocation.randomise()
            pchoice.assert_called_once_with(['A', 'B'])
            self.assertEqual('A', allocation.group)

    def test_already_random(self):
        "Raises"
        allocation = models.SingleUserAllocation(group="A")
        with self.assertRaises(exceptions.AlreadyRandomisedError):
            allocation.randomise()

if __name__ == '__main__':
    unittest.main()
