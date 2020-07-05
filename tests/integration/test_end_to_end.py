

def test_sending_an_order_returns_the_approved_url():
    # GIVEN a paypal client
    pc = paypalclient.PayPalClient()

    # GIVEN the paypal response
    paypal_response = paypalhttp.http_response.HttpResponse(
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

    # WHEN converting it to a dict
    result = pc.object_to_json(paypal_response)

    # THEN it is a python dict
    assert result == {
        'id': '7032651F',
        'intent': 'CAPTURE',
        'purchase_units': [
            {'reference_id': 'default', 'amount': {'currency_code': 'USD', 'value': '100.00'},
             'payee': {'email_address': '91603@business.example.com', 'merchant_id': 'xxx'},
             'shipping': {'method': 'DHL', 'name': {'full_name': 'Bob Buyer'},
                          'address': {'address_line_1': '123 St', 'admin_area_2': 'admin_area', 'postal_code': '33596',
                                      'country_code': 'US'}}}], 'create_time': '2020-07-04T17:28:59Z', 'links': [
            {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/651F', 'rel': 'self',
             'method': 'GET'},
            {'href': 'https://www.sandbox.paypal.com/checkoutnow?token=651F', 'rel': 'approve',
             'method': 'GET'},
            {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/651F', 'rel': 'update',
             'method': 'PATCH'},
            {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/651F/capture', 'rel': 'capture',
             'method': 'POST'}], 'status': 'CREATED'
    }