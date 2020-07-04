from datetime import datetime

from paypalcheckoutsdk.core import SandboxEnvironment, LiveEnvironment
import paypalhttp
import pytest

from paypalv2 import paypalclient


def test_default_settings_are_set_as_expected():
    # GIVEN the settings

    # WHEN

    # THEN
    pytest.fail('not completed!')


def test_paypal_environment_set_to_live_sets_the_environment_to_live_environment(mocker):
    # GIVEN we are in a live environment
    mocker.patch.object(paypalclient, 'PAYPAL_ENVIRONMENT', 'live')

    # WHEN instantiating a paypal client
    pc = paypalclient.PayPalClient()

    # THEN the environment is live
    assert isinstance(pc.environment, LiveEnvironment)


def test_paypal_environment_not_set_to_live_sets_the_environment_to_sandbox_environment(mocker):
    # GIVEN we are in a test environment
    mocker.patch.object(paypalclient, 'PAYPAL_ENVIRONMENT', 'sandbox')

    # WHEN instantiating a paypal client
    pc = paypalclient.PayPalClient()

    # THEN the environment is test/sandbox
    assert isinstance(pc.environment, SandboxEnvironment)


def test_serializing_the_paypal_response_into_python_types():
    """Github Issue #8 https://github.com/ThorstenMauch/oscar-paypalcheckout/issues/8"""
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
             'payee': {'email_address': 'c1891603@business.example.com', 'merchant_id': 'xxx'},
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
