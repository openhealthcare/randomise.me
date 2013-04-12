"""
Tests for custom Trial forms
"""
import unittest

from lxml import html

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
