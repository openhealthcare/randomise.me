"""
Unittests for Trial views
"""
from django import test
from django.test import Client
from lxml import html

from rm.trials import views

class CreateRMTrialTestCase(test.TestCase):

    def test_form_action(self):
        "Regression test #33"
        c = Client()
        with self.settings(BASICAUTH=False):
            resp = c.get('/trials/rm/new')
            self.assertEqual(200, resp.status_code)
            dom = html.fromstring(resp.content)
            form = dom.cssselect('form')[0]
            self.assertEqual('', form.get('action'))


class JoinTrialTestCase(test.TestCase):
    "Joining a trial"

    def test_get(self):
        "Joins Trial"
        pass
