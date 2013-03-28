"""
Context processors for Randomise Me
"""
from django.conf import settings

def sett(request):
    md = {}
    for x in dir(settings):
        md[x] = getattr(settings, x)
    return md
