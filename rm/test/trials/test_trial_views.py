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
           start_date=td(),
           finish_date=td(),
           max_participants=1,
           min_participants=1
           )

       trial.save()
       with self.settings(BASICAUTH=False):
           response = self.client.get('/trials/rm/1')
           self.assertEqual(200, response.status_code)


class CreateRMTrialTestCase(test.TestCase):

    def test_form_action(self):
        "Regression test #33"
        myuser = RMUser(email='larry@example.com')
        myuser.set_password('thepass')
        myuser.save()
        self.client.login(username='larry@example.com', password='thepass')

        with self.settings(BASICAUTH=False):
            resp = self.client.get('/trials/rm/new')
            self.assertEqual(200, resp.status_code)
            dom = html.fromstring(resp.content)
            form = dom.cssselect('form#newtrial_form')[0]
            self.assertEqual('', form.get('action'))


class JoinTrialTestCase(test.TestCase):
    "Joining a trial"

    def test_get(self):
        "Joins Trial"
        pass
