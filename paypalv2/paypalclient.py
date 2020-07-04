"""
https://developer.paypal.com/docs/api/orders/v2/
"""
import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalhttp import HttpResponse
from django.conf import settings

PAYPAL_CLIENT_ID = getattr(settings, 'PAYPAL_CLIENT_ID', 'Client id not set')
PAYPAL_CLIENT_SECRET = getattr(settings, 'PAYPAL_CLIENT_SECRET', 'client secret not set')
PAYPAL_ENVIRONMENT = getattr(settings, 'PAYPAL_ENVIRONMENT', 'sandbox')
PAYPAL_DEBUG = getattr(settings, 'PAYPAL_DEBUG', True)


class PayPalClient:
    """
    Returns PayPal HTTP client instance with environment that has access credentials context.
    Use this instance to invoke PayPal APIs, provided the credentials have access.
    """

    def __init__(self):
        self.client_id = PAYPAL_CLIENT_ID
        self.client_secret = PAYPAL_CLIENT_SECRET

        # choose live or sandbox Environment
        if PAYPAL_ENVIRONMENT == 'live':
            self.environment = LiveEnvironment(
                client_id=self.client_id, client_secret=self.client_secret)
        else:
            self.environment = SandboxEnvironment(
                client_id=self.client_id, client_secret=self.client_secret)

        self.client = PayPalHttpClient(self.environment)

    def response_to_dict(self, response: HttpResponse) -> dict:
        """
        Function to print all json data in an organized readable manner
        """
        return response.result.dict()

