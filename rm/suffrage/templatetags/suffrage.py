"""
Templatetags for the voting widget.
"""
from django import template

register = template.Library()

from rm.suffrage.models import Vote

@register.inclusion_tag('suffrage/voting_widget.html', takes_context=True)
def voting_widget(context, obj):
    """
    Render the voting widget for a particular object.
    """
    has_voted, val = False, None
    user = context['request'].user
    if user.is_authenticated():
        vote = obj.suffrage.vote_by(user)
        if vote:
            has_voted = True
            val = vote.val

    return dict(
        up=Vote.PLUS_ONE,
        down=Vote.MINUS_ONE,
        object=obj,
        has_voted=has_voted,
        vote=vote,
        )
