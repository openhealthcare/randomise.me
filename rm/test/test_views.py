"""
Tests for the top level, non app-specific views
"""
from django import test
from django.test.client import Client

class DisclaimerTestCase(test.TestCase):
    "Make sure the disclaimer functions"

    def test_disclaimer_resp_code(self):
        "Should be 200 refs #20"
        c = Client()
        with self.settings(BASICAUTH=False):
            resp = c.get('/disclaimer')
            self.assertEqual(200, resp.status_code)
