"""
Make things jsonish
"""
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.template import Library

register = Library()

def json(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return simplejson.dumps(object)

register.filter('json', json)
