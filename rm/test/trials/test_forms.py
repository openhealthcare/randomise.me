"""
Tests for custom Trial forms
"""
import unittest

from lxml import html
from mock import MagicMock

from rm.trials import forms

class BootstrapDatepickerWidgetTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_render(self):
        "Do we render with the correct markup?"
        widget = forms.BootstrapDatepickerWidget()
        output = widget.render('somedate', '')
        dom = html.fromstring(output)

        self.assertEqual("16", dom.cssselect('input')[0].get('size'))
        self.assertEqual("text", dom.cssselect('input')[0].get('type'))
        classy = dom.cssselect('div')[0].get('class').split()
        self.assertTrue("datepicker" in classy)

    def test_use_value(self):
        "Does the widget use the passed value argument?"
        widget = forms.BootstrapDatepickerWidget()
        output = widget.render('somedate', '22/12/1984')
        dom = html.fromstring(output)
        self.assertEqual('22/12/1984', dom.cssselect('input')[0].get('value'))

    def test_set_default(self):
        "Set default function"
        mock_dat = MagicMock(name="Mock Date Default")
        widget = forms.BootstrapDatepickerWidget(default=mock_dat)
        output = widget.render('somedate', '22/12/1984')
        mock_dat.assert_called_once_with()
