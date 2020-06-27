from decimal import Decimal as D

import pytest

from paypalv2 import gateway


@pytest.fixture
def test_order(mocker):
    return mocker.Mock(currency="USD", incl_tax=D('100'))


@pytest.fixture
def test_address(mocker):
    return mocker.Mock(
        first_name="Bob", last_name="Buyer", line1='123 St', line3=None,
        line4='admin_area', postcode='33596', country=mocker.Mock(code='US'))


def test_build_request_body_returns_expected_json(test_order, test_address):
    # GIVEN a create paypal order client
    order_client = gateway.CreatePaypalOrder()

    # WHEN building the request body
    request_body = order_client.build_request_body(
        order_number='1001', order_total=test_order, shipping_address=test_address)

    # THEN the body is as expected
    assert request_body == dict(
        intent="CAPTURE", application_context=dict(
            return_url="example.com/success/1001",
            cancel_url="example.com/cancel/1001",
            brand_name='Test Company',
            landing_page="BILLING",
            shipping_preference="SET_PROVIDED_ADDRESS",
            user_action="CONTINUE"
        ), purchase_units=[dict(
            amount=dict(
                currency_code="USD",
                value='100'
            ),
            shipping=dict(
                method="DHL",
                name=dict(full_name="Bob Buyer"),
                address=dict(
                    address_line_1="123 St", address_line_2=None, admin_area_2="admin_area",
                    postal_code="33596", country_code="US")
            )
        )]
    )


def test_build_request_body_for_delivery_of_a_halloween_box_with_preview_page(test_order, test_address):
    # GIVEN a create paypal order client
    order_client = gateway.CreatePaypalOrder()

    # WHEN building the request body
    request_body = order_client.build_request_body(
        order_number='1001', order_total=test_order, shipping_address=test_address)

    # THEN the body is as expected
    assert request_body == dict(
        intent="CAPTURE", application_context=dict(
            return_url="example.com/success/1001",
            cancel_url="example.com/cancel/1001",
            landing_page="BILLING",
            shipping_preference="SET_PROVIDED_ADDRESS",
            user_action="PAY_NOW"
        ), purchase_units=[dict(
            description="Halloween Box",
            invoice_id="TEST ORDER NUMBER",
            amount=dict(currency_code="USD", value='100'),
            shipping=dict(
                method="Delivery",
                name=dict(full_name="Bob Buyer"),
                address=dict(
                    address_line_1="123 St", address_line_2=None, admin_area_2="admin_area",
                    postal_code="33596", country_code="US")
            )
        )]
    )


def test_build_request_body_when_authorizing_payment(mocker):
    pytest.fail('not completed!')


def test_getting_application_context_returns_expected_dict():
    # GIVEN

    # WHEN

    # THEN
    pytest.fail('not completed!')


def test_getting_shipping_address_returns_expected_values():
    # GIVEN

    # WHEN

    # THEN
    pytest.fail('not completed!')


def test_getting_name_returns_expected_value():
    # GIVEN

    # WHEN

    # THEN
    pytest.fail('not completed!')


def test_create_order_returns_link():
    # GIVEN

    # WHEN

    # THEN
    pytest.fail('not completed!')


## Sample code from paypal
#
# def build_request_body():
#     """Method to create body with CAPTURE intent"""
#     return \
#         {
#             "intent": "CAPTURE",
#             "application_context": {
#                 "return_url": "https://www.example.com",
#                 "cancel_url": "https://www.example.com",
#                 "brand_name": "EXAMPLE INC",
#                 "landing_page": "BILLING",
#                 "shipping_preference": "SET_PROVIDED_ADDRESS",
#                 "user_action": "CONTINUE"
#             },
#
#             "intent": "CAPTURE",
#             "application_context": {
#                 "return_url": "someurl",
#                 "cancel_url": "someurl",
#                 "brand_name": "Some Brand",
#                 "landing_page": "BILLING",
#                 "shipping_preference": "SET_PROVIDED_ADDRESS",
#                 "user_action": "CONTINUE"
#             },
#
#             "purchase_units": [
#                 {
#                     "reference_id": "PUHF",
#                     "description": "Sporting Goods",
#
#                     "custom_id": "CUST-HighFashions",
#                     "soft_descriptor": "HighFashions",
#                     "amount": {
#                         "currency_code": "USD",
#                         "value": "220.00",
#                         "breakdown": {
#                             "item_total": {
#                                 "currency_code": "USD",
#                                 "value": "180.00"
#                             },
#                             "shipping": {
#                                 "currency_code": "USD",
#                                 "value": "20.00"
#                             },
#                             "handling": {
#                                 "currency_code": "USD",
#                                 "value": "10.00"
#                             },
#                             "tax_total": {
#                                 "currency_code": "USD",
#                                 "value": "20.00"
#                             },
#                             "shipping_discount": {
#                                 "currency_code": "USD",
#                                 "value": "10"
#                             }
#                         }
#                     },
#                     "items": [
#                         {
#                             "name": "T-Shirt",
#                             "description": "Green XL",
#                             "sku": "sku01",
#                             "unit_amount": {
#                                 "currency_code": "USD",
#                                 "value": "90.00"
#                             },
#                             "tax": {
#                                 "currency_code": "USD",
#                                 "value": "10.00"
#                             },
#                             "quantity": "1",
#                             "category": "PHYSICAL_GOODS"
#                         },
#                         {
#                             "name": "Shoes",
#                             "description": "Running, Size 10.5",
#                             "sku": "sku02",
#                             "unit_amount": {
#                                 "currency_code": "USD",
#                                 "value": "45.00"
#                             },
#                             "tax": {
#                                 "currency_code": "USD",
#                                 "value": "5.00"
#                             },
#                             "quantity": "2",
#                             "category": "PHYSICAL_GOODS"
#                         }
#                     ],
#                     "shipping": {
#                         "method": "United States Postal Service",
#                         "name": {
#                             "full_name": "John Doe"
#                         },
#                         "address": {
#                             "address_line_1": "123 Townsend St",
#                             "address_line_2": "Floor 6",
#                             "admin_area_2": "San Francisco",
#                             "admin_area_1": "CA",
#                             "postal_code": "94107",
#                             "country_code": "US"
#                         }
#                     }
#                 }
#             ]
#         }
#
#
# json_data: {
#     "intent": "CAPTURE",
#     "application_context": {
#         "return_url": "someurl",
#         "cancel_url": "someurl",
#         "brand_name": "Some Brand",
#         "landing_page": "BILLING",
#         "shipping_preference": "SET_PROVIDED_ADDRESS",
#         "user_action": "CONTINUE"
#     },
#     "purchase_units": [
#         {
#             "amount": {
#                 "currency_code": "EUR",
#                 "value": 40.09
#             },
#             "shipping": {
#                 "method": "DHL",
#                 "name": {
#                     "full_name": "John  Boime"
#                 },
#                 "address": {
#                     "address_line_1": "Somestreet. 50",
#                     "address_line_2": "2. haus rechts",
#                     "admin_area_2": "Hamburg",
#                     "postal_code": "21035",
#                     "country_code": "DE"
#                 }
#             }
#         }
#     ]
# }
