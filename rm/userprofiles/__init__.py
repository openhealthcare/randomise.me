"""
Add some signals to send notifications.
"""
from django.contrib.comments.signals import comment_was_posted

from rm.userprofiles.tasks import notify_new_comment

def comment_notification(sender, comment, request, **kw):
    """
    Send comment notifications to the user owning this trial
    (Actually, hand off to the task queue)

    Arguments:
    - `sender`:  model
    - `comment`: Comment
    - `request`: Request

    Return: None
    Exceptions: None
    """
    notify_new_comment.delay(comment.object_pk, comment.pk)
    return

comment_was_posted.connect(comment_notification)
