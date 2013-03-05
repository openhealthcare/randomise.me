"""
Custom defined exceptions for the Randomise.me project
"""
class Error(Exception):
    """
    Base class from which all Randomise.me errors inherit
    """

class TooManyParticipantsError(Error):
    """
    There are too many participants!
    """

class AlreadyJoinedError(Error):
    """
    A user tried to join a trial twice - sounds wonky to me.
    """

class TrialOwnerError(Error):
    """
    The trial owner attempted something they shouldn't
    """

class TrialFinishedError(Error):
    """
    This trial has finished. Some actions now impossible.
    """
