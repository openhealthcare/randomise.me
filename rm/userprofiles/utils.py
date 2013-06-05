"""
Utilities for creating users (Inteface for Django Allauth for now)
"""

from allauth.account.forms import SignupForm

def sign_me_up(request, email, pw1, pw2):
    """
    Given data for the signup form from somewhere, sign up a user
    and return that user.

    Arguments:
    - `request`: Request
    - `email`: str
    - `pw1`: str
    - `pw2`: str

    Return: RMUser or form with errors (Wonky behaviour, but this shouldn't happen...)
    Exceptions: None
    """
    form = SignupForm(data=dict(email=email, password1=pw1, password2=pw2))
    if form.is_valid():
        return form.save(request)
    return form
