from oscar.apps.checkout import views
from oscar.core.loading import get_class
from paypalv2.gateway import CreatePaypalOrder

RedirectRequired = get_class("payment.exceptions", "RedirectRequired")


class PaymentDetailsView(views.PaymentDetailsView):
    def handle_payment(self, order_number, total, **kwargs):
        if self.checkout_session.payment_method() == "paypal":
            frozen_basket = self.get_submitted_basket()
            shipping_address = self.get_shipping_address(frozen_basket)
            pp_order = CreatePaypalOrder()
            pp_link = pp_order.create_order(order_number, total, shipping_address)
            raise RedirectRequired(pp_link)
