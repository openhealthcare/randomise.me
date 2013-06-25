"""
Views to enable voting on Django model objects
"""
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.views.generic import View

from rm.suffrage.models import Vote

class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )


class VoteView(View):
    """
    Generic view for voting on a Django object.
    """
    def dispatch(self, *args, **kwargs):
        """
        Store model class

        Return: None
        Exceptions: None
        """
        self.contenttype = ContentType.objects.get(pk=kwargs['contenttype'])
        self.modelklass = self.contenttype.model_class()
        return super(VoteView, self).dispatch(*args, **kwargs)

    def get_object_or_404(self, pk):
        """
        Given the PK of our object, return that model instance or
        raise 404 Not found.

        Arguments:
        - `pk`: int

        Return: ModelBase
        Exceptions: Http404
        """
        try:
            return self.modelklass.objects.get(pk=pk)
        except self.modelklass.DoesNotExist:
            raise Http404

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        """
        Vote on this object.

        If the user has already voted on this object, do not allow them to
        vote twice.

        Return: HttpResponse
        Exceptions: None
        """
        obj = self.get_object_or_404(kwargs['pk'])
        val = self.request.POST.get('vote')
        vote, new = Vote.objects.get_or_create(content_type=self.contenttype,
                                             object_id=obj.pk,
                                             voter=self.request.user,
                                             defaults={'val': val})
        if not new:
            vote.val = val
            vote.save()

        if self.request.is_ajax():
            return JsonResponse(dict(error=None, vote=val))
        return HttpResponseRedirect(obj.get_absolute_url())

    def get(self, *args, **kwargs):
        """
        Return to object or 404
        """
        return HttpResponseRedirect(self.get_object_or_404(kwargs['pk']).get_absolute_url())
