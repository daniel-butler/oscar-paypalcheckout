import paypalhttp

from paypalv2 import paypalclient
from oscar.apps.checkout import views

from paypalv2.gateway import CreatePaypalOrder


def test_sending_an_order_returns_the_approved_url(mocker, test_address, test_order):
    # GIVEN Redirect link is mocked
    redirect_required_mock = mocker.Mock()

    # GIVEN a payment details view
    class PaymentDetailsView(views.PaymentDetailsView):

        checkout_session = mocker.Mock()

        def handle_payment(self, order_number, total, **kwargs):
            # GIVEN the payment method is paypal
            # frozen_basket = self.get_submitted_basket()
            # shipping_address = self.get_shipping_address(frozen_basket)
            pp_order = CreatePaypalOrder()

            pp_order.client = mocker.Mock(
                execute=mocker.Mock(
                    return_value=paypalhttp.http_response.HttpResponse(
                        data={
                            'id': '7032651F', 'intent': 'CAPTURE', 'purchase_units': [{
                                'reference_id': 'default',
                                'amount': {'currency_code': 'USD', 'value': '100.00'},
                                'payee': {'email_address': '91603@business.example.com', 'merchant_id': 'xxx'},
                                'shipping': {
                                    'method': 'DHL', 'name': {'full_name': 'Bob Buyer'},
                                    'address': {
                                        'address_line_1': '123 St',
                                        'admin_area_2': 'admin_area',
                                        'postal_code': '33596',
                                        'country_code': 'US'
                                    }
                                }
                            }],
                            'create_time': '2020-07-04T17:28:59Z', 'links': [
                                {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/651F', 'rel': 'self',
                                 'method': 'GET'},
                                {'href': 'https://www.sandbox.paypal.com/checkoutnow?token=651F', 'rel': 'approve',
                                 'method': 'GET'},
                                {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/651F', 'rel': 'update',
                                 'method': 'PATCH'},
                                {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/651F/capture',
                                 'rel': 'capture', 'method': 'POST'}
                            ], 'status': 'CREATED'},
                        status_code=201,
                        headers={
                            'Cache-Control': 'max-age=0, no-cache, no-store, must-revalidate',
                            'Content-Length': '917',
                            'Content-Type': 'application/json',
                            'Date': 'Sat, 04 Jul 2020 17:28:59 GMT',
                            'Paypal-Debug-Id': 'd5cd'
                        },
                    )
                ))
            pp_link = pp_order.create_order(order_number, test_order, test_address)
            return pp_link

    # GIVEN
    pdv = PaymentDetailsView()

    # GIVEN a paypal client
    pc = paypalclient.PayPalClient()

    # WHEN converting it to a dict
    pdv.handle_payment(1001, 100)

    # THEN it returns the paypal approved link
    assert redirect_required_mock.call_args[0] == 'https://www.sandbox.paypal.com/checkoutnow?token=651F'
