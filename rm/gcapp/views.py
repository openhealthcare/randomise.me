"""
Views for our Go Cardless integration
"""
from django.views.generic import RedirectView, TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.utils import simplejson

import gocardless

__all__ = ('Purchase', 'Subscribe', 'Preauth',
           'Confirm', 'Success', 'Error', 'Webhook')

gocardless.set_details(
    app_id='46V5WM1DYSDE62QXCJ42JT1KSZQRK772H8JGARTTTNCGCS34RFQTFM3CJY2G7FVG',
    app_secret='1GBC40E6JS4E0F2ZKV3NVH33KNX0CW4TS5AMV947FAGKFGXVX1SVW25G1PXKQET0',
    access_token='2E60XRDN5BME46X1G05ZWXDTFT71D339SB6Y3RDH0KTAG22Q0033Q403EMFDGBJW',
    merchant_id='0BF5SJEGEH'
)
gocardless.environment = 'sandbox'

User = get_user_model()


# Generate a URL for a one-off payment and redirect to it
class Purchase(RedirectView):
    def get_redirect_url(self, **kwargs):
        url = gocardless.client.new_bill_url(
            10,
            name=self.request.POST.get('name')
        )
        return url


# Generate a URL for a subscription and redirect to it
class Subscribe(RedirectView):
    def get_redirect_url(self, **kwargs):
        url = gocardless.client.new_subscription_url(
            20,
            interval_unit='month',
            interval_length=1,
            name=self.request.POST.get('name')
        )
        return url


# Generate a URL for a preauthorization and redirect to it
class Preauth(RedirectView):
    def get_redirect_url(self, **kwargs):
        url = gocardless.client.new_preauthorization_url(
            100,
            interval_unit='month',
            interval_length=3,
            name=self.request.POST.get('name'),
        )
        return url


# Handle the callback after the user finishes the payment process.
# Render a success/error page depending on whether the transaction
# was successful or not.
# https://gocardless.com/docs/python/merchant_client_guide#completing-the-payment
class Confirm(RedirectView):
    query_string = True

    def get_redirect_url(self, **kwargs):
        try:
            gocardless.client.confirm_resource(self.request.GET)
            # If we've confirmed, we should update the user's account here.
            if self.request.user.is_authenticated():
                self.request.user.upgrade()
            self.url = reverse_lazy('gc_success')
        except Exception:
            self.url = reverse_lazy('gc_error')

        return super(Confirm, self).get_redirect_url(**kwargs)


# Simple success and error views
class Success(TemplateView):
    template_name = 'gcapp/success.html'

class Error(TemplateView):
    template_name = 'error.html'


# Handle the incoming Webhook and perform an action with the
# Webhook data.
# More information at https://gocardless.com/docs/web_hooks_guide
class Webhook(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Webhook, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_data = simplejson.loads(request.raw_post_data)
        webhook_data = incoming_data.get('payload')

        if gocardless.client.validate_webhook(webhook_data):
            # Do something with webhook_data, save to DB, log etc
            # For example, if you had a model called Bill and you want
            # to update each of the incoming bills
            # for b in webhook_data['bills']:
            #   bill = Bill.get(id=b['id'])
            #   bill.status = b['status']
            #   bill.save()
            pass
        else:
            # log the error
            pass

        return HttpResponse()
