"""
Unittests for Trial views
"""
import datetime

from django import test
from lxml import html

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
        self.client.login(username='larry', password='thepass')

        with self.settings(BASICAUTH=False):
            resp = self.client.get('/trials/create')
            self.assertEqual(200, resp.status_code)
            dom = html.fromstring(resp.content)
            form = dom.cssselect('form#newtrial_form')[0]
            self.assertEqual('/trials/create', form.get('action'))


class JoinTrialTestCase(test.TestCase):
    "Joining a trial"

    def test_get(self):
        "Joins Trial"
        pass
