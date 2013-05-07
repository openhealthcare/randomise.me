"""
Unittests for the GO Cardless integration
"""
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from mock import patch

from rm.gcapp import views

def raiser(exc):
    "Mock helper"
    def raisee(*args, **kwargs):
        raise exc()
    return raisee

class GoCardlessTest(TestCase):
    # These are slightly modified from the gocardless sample app tests.
    # https://github.com/gocardless/sample-django-app
    def test_index(self):
        with self.settings(BASICAUTH=False):
            response = self.client.get('/gocardless/')

            self.assertEqual(response.status_code, 200)
            self.assertTrue('GoCardless sample application' in response.content)

    def test_buy(self):
        with self.settings(BASICAUTH=False):
            response = self.client.post('/gocardless/buy/', {'name': 'Test'})

            self.assertEqual(response.status_code, 301)
            self.assertTrue('https://sandbox.gocardless.com/connect/bills/new' in
                            response['Location'])

    def test_subscription(self):
        with self.settings(BASICAUTH=False):
            response = self.client.post('/gocardless/subscribe/', {'name': 'Test'})

            self.assertEqual(response.status_code, 301)
            self.assertTrue('https://sandbox.gocardless.com/connect/subscriptions/new' in
                            response['Location'])

    def test_preauth(self):
        with self.settings(BASICAUTH=False):
            response = self.client.post('/gocardless/preauth/', {'name': 'Test'})

            self.assertEqual(response.status_code, 301)
            self.assertTrue('https://sandbox.gocardless.com/connect/pre_authorizations/new' in
                            response['Location'])


class ConfirmTestCase(TestCase):
    """
    Our payment confirmation view
    """

    def test_confirm_correct(self):
        " 301 success "
        with self.settings(BASICAUTH=False):
            with patch.object(views.gocardless.client, 'confirm_resource') as pconf:
                self.client.get('/gocardless/confirm/')
                pconf.assert_called_once_with({})


    def test_confirm_fail(self):
        " 301 failure "
        with self.settings(BASICAUTH=False):
            with patch.object(views.gocardless.client, 'confirm_resource') as pconf:
                self.client.get('/gocardless/confirm/')
                pconf.assert_called_once_with({})
