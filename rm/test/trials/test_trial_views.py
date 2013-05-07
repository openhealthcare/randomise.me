"""
Unittests for Trial views
"""
from django import test
from lxml import html

from rm.trials import views

class DetailTestCase(test.TestCase):

    def test_200_not_logged_in(self):
       " Assert status Regression #60"
       with self.settings(BASICAUTH=False):
           response = self.client.get('/trials/rm/1')
           self.assertEqual(200, response.status_code)


class CreateRMTrialTestCase(test.TestCase):

    def test_form_action(self):
        "Regression test #33"
        with self.settings(BASICAUTH=False):
            resp = self.client.get('/trials/rm/new')
            self.assertEqual(200, resp.status_code)
            dom = html.fromstring(resp.content)
            form = dom.cssselect('form')[0]
            self.assertEqual('', form.get('action'))


class JoinTrialTestCase(test.TestCase):
    "Joining a trial"

    def test_get(self):
        "Joins Trial"
        pass
