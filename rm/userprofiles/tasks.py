"""
Tasks for user-related actions
"""
from celery import task
from django.conf import settings
from django.contrib.comments.models import Comment
import letter

from rm.userprofiles.models import RMUser
from rm.trials.models import Trial

POSTIE = letter.DjangoPostman()

@task
def notify_new_comment(trial_pk, comment_pk):
    """
    Given the user, trial, and comment ids, notify the user that
    a new comment has been made on their trial.

    Arguments:
    - `user_pk`: int
    - `trial_pk`: int
    - `comment_pk`: int

    Return: None
    Exceptions: None
    """
    comment = Comment.objects.get(pk=comment_pk)
    trial = Trial.objects.get(pk=trial_pk)
    owner = trial.owner

    class Message(letter.Letter):
        Postie   = POSTIE

        From     = settings.DEFAULT_FROM_EMAIL
        To       = owner.email
        Subject  = 'Randomise Me - New comment on {0}'.format(trial.title)
        Template = 'email/new_trial_comment'
        Context  = {
            'title'       : trial.title,
            'comment_from': comment.email,
            'comment_text': comment.comment,
            'trial_href'  : settings.DEFAULT_DOMAIN + comment.get_absolute_url()
            }

    print 'sending'
    owner.send_message(Message)

    return
