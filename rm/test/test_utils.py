"""
Unittests for the rm.utils module
"""
import datetime
import unittest

import mock
from mock import patch, MagicMock

from rm import utils

class MockedToday(unittest.TestCase):
    "Mock today please"

    def setUp(self):
        date_patcher = mock.patch.object(
            utils.datetime, 'date',
            mock.Mock(wraps=datetime.date)
            )
        mocked_date = date_patcher.start()
        mocked_date.today.return_value = datetime.date(1984, 12, 22)

        self.addCleanup(date_patcher.stop)


class TodayTestCase(MockedToday):
    def tearDown(self):
        pass

    def test_today(self):
        "Format today's date nicely"
        self.assertEqual('22/12/1984', utils.today())

class InATestCase(MockedToday):
    "Futures API"

    def test_in_a_week(self):
        "One week in the future?"
        self.assertEqual('29/12/1984', utils.in_a(week=1))
