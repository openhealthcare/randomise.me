"""
Unittests for the GO Cardless integration
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, utils

from mock import patch

from rm.gcapp import views
from rm.userprofiles.models import RMUser
from rm.test import rmtestutils

def setup_module(module):
    rmtestutils.setup_module(module)
    module.oldauth = settings.BASICAUTH
    settings.BASICAUTH = False

def teardown_module(module):
    rmtestutils.teardown_module(module)
    settings.BASICAUTH = module.oldauth

def raiser(exc):
    "Mock helper"
    def raisee(*args, **kwargs):
        raise exc()
    return raisee

class GoCardlessTest(TestCase):
    # These are slightly modified from the gocardless sample app tests.
    # https://github.com/gocardless/sample-django-app
    def test_index(self):
        response = self.client.get('/gocardless/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('GoCardless sample application' in response.content)

    def test_buy(self):
        response = self.client.post('/gocardless/buy/', {'name': 'Test'})

        self.assertEqual(response.status_code, 301)
        self.assertTrue('https://sandbox.gocardless.com/connect/bills/new' in
                        response['Location'])

    def test_subscription(self):
        response = self.client.post('/gocardless/subscribe/', {'name': 'Test'})

        self.assertEqual(response.status_code, 301)
        self.assertTrue('https://sandbox.gocardless.com/connect/subscriptions/new' in
                        response['Location'])

    def test_preauth(self):
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
        with patch.object(views.gocardless.client, 'confirm_resource') as pconf:
            resp = self.client.get('/gocardless/confirm/')
            pconf.assert_called_once_with({})
            self.assertEqual(301, resp.status_code)
            self.assertIn(reverse('gc_success'), resp['Location'])

    def test_confirm_fail(self):
        " 301 failure "
        with patch.object(views.gocardless.client, 'confirm_resource') as pconf:
            pconf.side_effect = raiser(Exception)
            resp = self.client.get('/gocardless/confirm/')
            pconf.assert_called_once_with({})
            self.assertEqual(301, resp.status_code)
            self.assertIn(reverse('gc_error'), resp['Location'])

    def test_subscribe_logged_in(self):
        "Should upgrade account"
        myuser = RMUser(username='larry', email='larry@example.com')
        myuser.set_password('thepass')
        myuser.save()
        self.assertTrue(self.client.login(username='larry@example.com', password='thepass'))
        GET = {'resource_type': 'subscription'}

        with patch.object(views.User, 'upgrade') as pup:
            with patch.object(views.gocardless.client, 'confirm_resource') as pconf:
                resp = self.client.get('/gocardless/confirm/', GET)
                pup.assert_called_once_with()
