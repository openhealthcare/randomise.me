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
