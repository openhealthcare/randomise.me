"""
Unittests for Form validators
"""
import datetime
import unittest

from rm.trials import validators

class NotHistoricTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_returns_true(self):
        "should return True"
        future = datetime.date.today() + datetime.timedelta(days=1)
        resp = validators.not_historic(future)
        self.assertEqual(True, resp)
