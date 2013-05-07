"""
Re-usable testing utilities for Randomise Me
"""
from django.core.management import call_command
from django import db
from django.test import utils
from django.test.simple import DjangoTestSuiteRunner

def setup_module(module):
    runner = DjangoTestSuiteRunner(interactive=False)
    module.config = runner.setup_databases()
    utils.setup_test_environment()
    try:
        call_command('migrate', interactive=False)
    except db.DatabaseError:
        pass


def teardown_module(module):
    runner = DjangoTestSuiteRunner(interactive=False)
    runner.teardown_databases(module.config)
