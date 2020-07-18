import sys
from importlib import reload, import_module
from decimal import Decimal as D

import pytest
from django.conf import settings
from django.test.utils import override_settings
from django.urls import reverse, clear_url_caches

from oscar.core.loading import get_class, get_model
from oscar.test import factories
from oscar.test.testcases import WebTestCase

RedirectRequired = get_class("payment.exceptions", "RedirectRequired")
UserAddress = get_model('address', 'UserAddress')
Country = get_model('address', 'Country')
GatewayForm = get_class('checkout.forms', 'GatewayForm')


class CheckoutMixin(object):

    def create_digital_product(self):
        product_class = factories.ProductClassFactory(
            requires_shipping=False, track_stock=False)
        product = factories.ProductFactory(product_class=product_class)
        factories.StockRecordFactory(
            num_in_stock=None, price_excl_tax=D('12.00'), product=product)
        return product

    def add_product_to_basket(self, product=None):
        if product is None:
            product = factories.ProductFactory()
            factories.StockRecordFactory(
                num_in_stock=10, price_excl_tax=D('12.00'), product=product)
        detail_page = self.get(product.get_absolute_url())
        form = detail_page.forms['add_to_basket_form']
        form.submit()

    def add_voucher_to_basket(self, voucher=None):
        if voucher is None:
            voucher = factories.create_voucher()
        basket_page = self.get(reverse('basket:summary'))
        form = basket_page.forms['voucher_form']
        form['code'] = voucher.code
        form.submit()

    def enter_guest_details(self, email='guest@example.com'):
        index_page = self.get(reverse('checkout:index'))
        index_page.form['username'] = email
        index_page.form.select('options', GatewayForm.GUEST)
        return index_page.form.submit()

    def create_shipping_country(self):
        return factories.CountryFactory(
            iso_3166_1_a2='GB', is_shipping_country=True)

    def enter_shipping_address(self):
        self.create_shipping_country()
        address_page = self.get(reverse('checkout:shipping-address'))
        form = address_page.forms['new_shipping_address']
        form['first_name'] = 'John'
        form['last_name'] = 'Doe'
        form['line1'] = '1 Egg Road'
        form['line4'] = 'Shell City'
        form['postcode'] = 'N12 9RT'
        form.submit()

    def enter_shipping_method(self):
        self.get(reverse('checkout:shipping-method'))

    def place_order(self):
        payment_details = self.get(
            reverse('checkout:shipping-method')).follow().follow()
        preview = payment_details.click(linkid="view_preview")
        return preview.forms['place_order_form'].submit().follow()

    def reach_payment_details_page(self, is_guest=False):
        self.add_product_to_basket()
        if is_guest:
            self.enter_guest_details('hello@egg.com')
        self.enter_shipping_address()
        return self.get(
            reverse('checkout:shipping-method')).follow().follow()

    def ready_to_place_an_order(self, is_guest=False):
        payment_details = self.reach_payment_details_page(is_guest)
        return payment_details.click(linkid="view_preview")


def reload_url_conf():
    """Reload URLs to pick up the overridden settings"""
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
    import_module(settings.ROOT_URLCONF)
    clear_url_caches()


@override_settings(OSCAR_ALLOW_ANON_CHECKOUT=True)
class TestPaymentCase(CheckoutMixin, WebTestCase):
    is_anonymous = True

    def setUp(self):
        reload_url_conf()
        super().setUp()

    def test_redirects_customer_with_empty_basket(self):
        response = self.get(reverse('checkout:index'))
        self.assertRedirectsTo(response, 'basket:summary')

    def test_shows_initial_data_if_the_form_has_already_been_submitted(self):
        self.add_product_to_basket()
        self.enter_guest_details('hey@you.com')
        self.enter_shipping_address()
        page = self.get(reverse('checkout:shipping-address'), user=self.user)

        assert page.form['first_name'].value == 'John'

    def test_handling_payment_calls_paypal_with_expected_values(self):
        self.add_product_to_basket()
        self.enter_guest_details('hey@you.com')
        self.enter_shipping_address()
        page = self.get(reverse('checkout:shipping-address'), user=self.user)

        assert page.form['first_name'].value == 'John'

    def test_saves_guest_email_with_order(self):
        preview = self.ready_to_place_an_order(is_guest=True)
        thank_you = preview.forms['place_order_form'].submit().follow()
        order = thank_you.context['order']
        assert order.guest_email == 'hello@egg.com'

    def test_submitting_a_paypal_payment(self):
        preview = self.ready_to_place_an_order(is_guest=True)

        preview

        # WHEN

        # THEN

        pytest.fail('not completed!')



