
from django.urls import reverse

from oscar.test.testcases import WebTestCase


class TestBasketSummaryView(WebTestCase):

    def setUp(self):
        url = reverse('basket:summary')
        self.response = self.app.get(url)

    def test_shipping_method_in_context(self):
        self.assertTrue('shipping_method' in self.response.context)
