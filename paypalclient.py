from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment

import sys
'''
https://developer.paypal.com/docs/api/orders/v2/
'''

from frobshop.settings import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, PAYPAL_ENVIRONMENT


class PayPalClient:
    def __init__(self):
        self.client_id = PAYPAL_CLIENT_ID
        self.client_secret = PAYPAL_CLIENT_SECRET

        # choose live or sandbox Environment
        if(PAYPAL_ENVIRONMENT  == 'live'):
            self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        else:

            self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__") or key.startswith("_"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result;
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result;

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, str) or isinstance(data, int)
