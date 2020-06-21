import pytest


def test_build_request_body_returns_expected_json():
    # GIVEN

    # WHEN

    # THEN
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
