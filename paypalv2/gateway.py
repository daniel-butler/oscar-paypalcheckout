import json
from typing import Optional, Union

from django.conf import settings
from .paypalclient import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

from paypalhttp.http_response import HttpResponse
from paypalhttp.http_error import HttpError

PAYPAL_SUCCESS_PAGE = getattr(settings, 'PAYPAL_SUCCESS_PAGE')
PAYPAL_CANCEL_PAGE = getattr(settings, 'PAYPAL_CANCEL_PAGE')
PAYPAL_BRAND_NAME = getattr(settings, 'PAYPAL_BRAND_NAME')
PAYPAL_DEBUG = getattr(settings, 'PAYPAL_DEBUG', True)


class CapturePaypalOrder(PayPalClient):
    def capture(self, paypal_order_id) -> Union[HttpResponse, HttpError]:
        request = OrdersCaptureRequest(paypal_order_id)
        # 3. Call PayPal to capture an order
        response = self.client.execute(request)
        if PAYPAL_DEBUG:
            json_data = self.object_to_json(response.result)
            print(json.dumps(json_data, indent=4))
        return response


class CreatePaypalOrder(PayPalClient):
    """
    Maybe is necessary to override the name and address details
    """

    def get_name(self, shipping_address) -> str:
        return shipping_address.first_name + " " + shipping_address.last_name

    def get_shipping_address(self, shipping_address) -> dict:
        return {
            "address_line_1": shipping_address.line1,  # street
            "address_line_2": shipping_address.line3,
            "admin_area_2": shipping_address.line4,  # City
            "postal_code": shipping_address.postcode,
            "country_code": shipping_address.country.code,
        }

    def get_application_context(self, orderno) -> dict:
        """
        @todo: Check if global vars are set

        """
        if PAYPAL_DEBUG:
            print("App context  Orderno " + str(orderno))

        return {
            "return_url": PAYPAL_SUCCESS_PAGE + str(orderno),
            "cancel_url": PAYPAL_CANCEL_PAGE + str(orderno),
            "brand_name": PAYPAL_BRAND_NAME,
            # unclear what this means and if it's necessary
            "landing_page": "BILLING",
            "shipping_preference": "SET_PROVIDED_ADDRESS",
            "user_action": "CONTINUE"
        }

    def build_request_body(self, order_number, order_total, shipping_address) -> dict:
        return {
            "intent": 'CAPTURE',
            "application_context": self.get_application_context(order_number),
            "purchase_units": [{
                "amount": {
                    # @todo  Currency is set fixed to Euro. must be replaced
                    "currency_code": order_total.currency,
                    "value": str(order_total.incl_tax),
                },
                "shipping": {
                    "method": "DHL",
                    "name": {
                        "full_name": self.get_name(shipping_address),
                    },
                    "address": self.get_shipping_address(shipping_address),
                },
            }]
        }

    def create_order(self, order_number, order_total, shipping_address) -> Optional[str]:
        """
        :param order_number: the Oscar Order Number
        :param order_total: total of the order
        :param shipping_address: shipping address oscar object
        :return: the approve link to redirect to paypal
        """
        request = OrdersCreateRequest()
        request.headers['prefer'] = 'return=representation'
        body = self.build_request_body(order_number, order_total, shipping_address)
        request.request_body(body)
        response = self.client.execute(request)

        if PAYPAL_DEBUG:
            json_data = self.object_to_json(response.result)
            print("json_data: ", json.dumps(json_data, indent=4))

        for link in response.result.links:
            if link.rel == "approve":
                return link.href


x = {
    "name": "INVALID_REQUEST",
    "message": "Request is not well-formed, syntactically incorrect, or violates schema.",
    "debug_id": "8c444c6b4038b",
    "details":
        [
            {"field": "/application_context/cancel_url",
             "value": "example.com/cancel/1001",
             "location": "body",
             "issue": "INVALID_PARAMETER_SYNTAX",
             "description": "The value of a field does not conform to the expected format."},
            {"field": "/application_context/return_url",
             "value": "example.com/success/1001",
             "location": "body",
             "issue": "INVALID_PARAMETER_SYNTAX",
             "description": "The value of a field does not conform to the expected format."}
        ],
    "links": [
        {"href": "https://developer.paypal.com/docs/api/orders/v2/#error-INVALID_PARAMETER_SYNTAX",
         "rel": "information_link", "encType": "application/json"}
    ]
}
'''

Sample code from paypal:

 def build_request_body():
    """Method to create body with CAPTURE intent"""
    return \
        {
            "intent": "CAPTURE",
            "application_context": {
                "return_url": "https://www.example.com",
                "cancel_url": "https://www.example.com",
                "brand_name": "EXAMPLE INC",
                "landing_page": "BILLING",
                "shipping_preference": "SET_PROVIDED_ADDRESS",
                "user_action": "CONTINUE"
            },
            
            "intent": "CAPTURE",
            "application_context": {
                "return_url": "someurl",
                "cancel_url": "someurl",
                "brand_name": "Some Brand",
                "landing_page": "BILLING",
                "shipping_preference": "SET_PROVIDED_ADDRESS",
                "user_action": "CONTINUE"
            },

            "purchase_units": [
                {
                    "reference_id": "PUHF",
                    "description": "Sporting Goods",

                    "custom_id": "CUST-HighFashions",
                    "soft_descriptor": "HighFashions",
                    "amount": {
                        "currency_code": "USD",
                        "value": "220.00",
                        "breakdown": {
                            "item_total": {
                                "currency_code": "USD",
                                "value": "180.00"
                            },
                            "shipping": {
                                "currency_code": "USD",
                                "value": "20.00"
                            },
                            "handling": {
                                "currency_code": "USD",
                                "value": "10.00"
                            },
                            "tax_total": {
                                "currency_code": "USD",
                                "value": "20.00"
                            },
                            "shipping_discount": {
                                "currency_code": "USD",
                                "value": "10"
                            }
                        }
                    },
                    "items": [
                        {
                            "name": "T-Shirt",
                            "description": "Green XL",
                            "sku": "sku01",
                            "unit_amount": {
                                "currency_code": "USD",
                                "value": "90.00"
                            },
                            "tax": {
                                "currency_code": "USD",
                                "value": "10.00"
                            },
                            "quantity": "1",
                            "category": "PHYSICAL_GOODS"
                        },
                        {
                            "name": "Shoes",
                            "description": "Running, Size 10.5",
                            "sku": "sku02",
                            "unit_amount": {
                                "currency_code": "USD",
                                "value": "45.00"
                            },
                            "tax": {
                                "currency_code": "USD",
                                "value": "5.00"
                            },
                            "quantity": "2",
                            "category": "PHYSICAL_GOODS"
                        }
                    ],
                    "shipping": {
                        "method": "United States Postal Service",
                        "name": {
                            "full_name":"John Doe"
                        },
                        "address": {
                            "address_line_1": "123 Townsend St",
                            "address_line_2": "Floor 6",
                            "admin_area_2": "San Francisco",
                            "admin_area_1": "CA",
                            "postal_code": "94107",
                            "country_code": "US"
                        }
                    }
                }
            ]
        }



json_data:  {
    "intent": "CAPTURE",
    "application_context": {
        "return_url": "someurl",
        "cancel_url": "someurl",
        "brand_name": "Some Brand",
        "landing_page": "BILLING",
        "shipping_preference": "SET_PROVIDED_ADDRESS",
        "user_action": "CONTINUE"
    },
    "purchase_units": [
        {
            "amount": {
                "currency_code": "EUR",
                "value": 40.09
            },
            "shipping": {
                "method": "DHL",
                "name": {
                    "full_name": "John  Boime"
                },
                "address": {
                    "address_line_1": "Somestreet. 50",
                    "address_line_2": "2. haus rechts",
                    "admin_area_2": "Hamburg",
                    "postal_code": "21035",
                    "country_code": "DE"
                }
            }
        }
    ]
}

'''
