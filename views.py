import json
import logging
from decimal import Decimal

from django.shortcuts import render
from django.views import generic
from oscar.apps.checkout import signals
from oscar.apps.payment.models import SourceType, Source
from oscar.core.loading import get_class
from paypalcheckout.paypalcommands import CapturePaypalOrder
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')


# Standard logger for checkout events
logger = logging.getLogger('oscar.checkout')

# only purpose is to have a common way to handel errors an return doe the preview
class PaypalView(OrderPlacementMixin, generic.TemplateView):
    template_name = 'oscar/checkout/preview.html'

    def cancel_transaction(self, msg):
        # restore frozen basket
        self.restore_frozen_basket()

        # and return to the preview and show a error message
        kwargs = {"error": msg}
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)


class PaypalCancelView(PaypalView):



    def get(self, request, *args, **kwargs):


        # restore frozen basket
        self.restore_frozen_basket()

        #and return to the preview and show a error message
        # @todo: needs translation
        kwargs = {"error": "Die Paypal Zahlung wurde abgebrochen"}
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)


class PaypalSuccessView(PaypalView):

    orderno = 0

    def get(self, request, *args, **kwargs):

        paypal_order_id =self.request.GET['token']

        pp_response =CapturePaypalOrder().capture(paypal_order_id)

        order_number=kwargs.get('orderno')

        # get the frozzen basket
        basket = self.get_submitted_basket()

        # Basket strategy needed to calculate prices
        # and the basket in session is stroed without  strategy
        # Use same strategy as current request basket, whitch
        # was created by the middleware
        basket.strategy = self.request.basket.strategy



        shipping_address = self.get_shipping_address(basket)
        shipping_method = self.get_shipping_method(
            basket, shipping_address)
        if not shipping_method:
            #  this should nbe impossible at this point
            # however we handle it
            total = shipping_charge = None
            raise Exception("shipping_method not set. Can't calculate order totals")
        else:
            shipping_charge = shipping_method.calculate(basket)
            order_total = self.get_order_totals(basket, shipping_charge=shipping_charge)

        # we should have exact one purchase_units  and one capture
        capture = pp_response.result.purchase_units[0].payments.captures[0]
        # check if paypal payment is completed and if the paypal payment matches the order total
        # this case should be impossible. However is a extra security  check

        if(capture.status != "COMPLETED"):
            msg ="Paypal Capture STATUS in not COMPLETED"
            logger.error(msg)
            return(self.cancel_transaction(msg))

        if(Decimal(capture.amount.value) != order_total.incl_tax):
            msg = "Paypal amount differ from order_total"
            logger.error(msg)
            return (self.cancel_transaction(msg))



        # Payment  now successful! Record payment source
        source_type, __ = SourceType.objects.get_or_create(
            name="Paypal")
        source = Source(
            source_type=source_type,
            amount_allocated=order_total.incl_tax,
            reference=pp_response.result.id)
        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('pre-auth', order_total.incl_tax)



        return (self.submit(order_number,order_total, basket, shipping_address, shipping_method, shipping_charge))



    def submit(self,order_number,order_total, basket, shipping_address, shipping_method, shipping_charge):
        '''
        basicly it perform the same steps as PaymentDetailsView.submit, after the redirect
        :param order_number:
        :return:
        '''


        billing_address = self.get_billing_address(shipping_address)
        order_kwargs ={}
        # raise the same signal, then in PaymentDetailsView.submit, i have now idea if this needed
        # and if it may have side effect under certain  circumstance
        # It may reviewed by someone with good understandig with ocscars signals
        signals.post_payment.send_robust(sender=self, view=self)
        response=self.handle_order_placement(
                        order_number, self.request.user, basket, shipping_address, shipping_method,
                shipping_charge, billing_address, order_total,  **order_kwargs)


        return response