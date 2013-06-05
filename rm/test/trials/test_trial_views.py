"""
Unittests for Trial views
"""
import datetime
import unittest

from django import test
from lxml import html
from mock import MagicMock

from rm.trials import views, models
from rm.userprofiles.models import RMUser
from rm.test import rmtestutils

td = datetime.date.today

setup_module = rmtestutils.setup_module
teardown_module = rmtestutils.teardown_module

class DetailTestCase(test.TestCase):

    def test_200_not_logged_in(self):
       " Assert status Regression #60"
       myuser = RMUser(email='larry@example.com')
       myuser.set_password('thepass')
       myuser.save()

       trial = models.Trial(
           owner=myuser,
           title='Dummy Trial',
           min_participants=1
           )

       trial.save()
       with self.settings(BASICAUTH=False):
           response = self.client.get('/trials/rm/1')
           self.assertEqual(200, response.status_code)

    def test_401_private_trial(self):
        "Ensure privacy"
        myuser = RMUser(email='larry@example.com')
        myuser.set_password('thepass')
        myuser.save()

        trial = models.Trial(
            owner=myuser,
            private=True,
            title='Dummy Trial',
            min_participants=1
            )

        trial.save()
        with self.settings(BASICAUTH=False):
            response = self.client.get('/trials/rm/{0}'.format(trial.pk))
            self.assertEqual(401, response.status_code)

    def test_200_private_trial_is_owner(self):
        "Ensure Privacy"
        myuser = RMUser(email='larry@example.com', username='larry')
        myuser.set_password('thepass')
        myuser.save()

        trial = models.Trial(
            owner=myuser,
            private=True,
            title='Dummy Trial',
            min_participants=1
            )
        trial.save()
        var = models.Variable(question='Why?', trial=trial)
        var.save()
        self.assertTrue(self.client.login(username='larry@example.com', password='thepass'))

        with self.settings(BASICAUTH=False):
            response = self.client.get('/trials/rm/{0}'.format(trial.pk))
            self.assertEqual(200, response.status_code)

    def test_200_private_trial_is_participant(self):
        "Ensure privacy"
        owner = RMUser(email='larry@example.com', username='larry')
        owner.save()
        part_user = RMUser(email='bill@example.com', username='bill')
        part_user.set_password('pass')
        part_user.save()

        trial = models.Trial(owner=owner, private=True, title='Foo', min_participants=1)
        trial.save()

        var = models.Variable(question='Why?', trial=trial)
        var.save()
        part = models.Participant(user=part_user, trial=trial)
        part.save()

        self.assertTrue(self.client.login(username='bill@example.com', password='pass'))

        with self.settings(BASICAUTH=False):
            response = self.client.get('/trials/rm/{0}'.format(trial.pk))
            self.assertEqual(200, response.status_code)

    def test_200_private_trial_is_invited(self):
        "Ensure privacy"
        owner = RMUser(email='larry@example.com', username='larry')
        owner.save()
        invitee = RMUser(email='bill@example.com', username='bill')
        invitee.set_password('pass')
        invitee.save()

        trial = models.Trial(owner=owner, private=True, title='Foo', min_participants=1)
        trial.save()

        var = models.Variable(question='Why?', trial=trial)
        var.save()
        invitation = models.Invitation(email=invitee.email, trial=trial, sent=True)
        invitation.save()

        self.assertTrue(self.client.login(username='bill@example.com', password='pass'))

        with self.settings(BASICAUTH=False):
            response = self.client.get('/trials/rm/{0}'.format(trial.pk))
            self.assertEqual(200, response.status_code)

    def test_401_private_n1_trial(self):
        "Ensure privacy controls"
        myuser = RMUser(email='larry@example.com')
        myuser.set_password('thepass')
        myuser.save()

        trial = models.Trial(
            owner=myuser,
            n1trial=True,
            private=True,
            title='Dummy Trial',
            min_participants=1
            )

        trial.save()
        with self.settings(BASICAUTH=False):
            response = self.client.get('/trials/rm/{0}'.format(trial.pk))
            self.assertEqual(401, response.status_code)



class CreateRMTrialTestCase(test.TestCase):

    def test_form_action(self):
        "Regression test #33"
        myuser = RMUser(email='larry@example.com', username='larry')
        myuser.set_password('thepass')
        myuser.save()
        self.client.login(username='larry@example.com', password='thepass')

        with self.settings(BASICAUTH=False):
            resp = self.client.get('/trials/create')
            self.assertEqual(200, resp.status_code)
            dom = html.fromstring(resp.content)
            form = dom.cssselect('form#newtrial_form')[0]
            self.assertEqual('/trials/create', form.get('action'))

class ReproduceTrialTestCase(unittest.TestCase):

    def test_context(self):
        "has vars"
        view = views.ReproduceTrial()
        view.object = view.parent = view.reproducee = MagicMock(name='Mock Trial')
        ctx = view.get_context_data()
        self.assertEqual(True, ctx['reproducing'])
        self.assertEqual(view.parent, ctx['parent'])

class ReproduceN1TrialTestCase(unittest.TestCase):

    def test_context(self):
        "has vars"
        view = views.ReproduceN1Trial()
        view.object = view.parent = view.reproducee = MagicMock(name='Mock Trial')
        ctx = view.get_context_data()
        self.assertEqual(True, ctx['reproducing'])
        self.assertEqual(True, ctx['n1trial'])
        self.assertEqual(view.parent, ctx['parent'])
