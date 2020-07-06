from decimal import Decimal as D
import os

import django
import pytest


def pytest_configure(config):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()


@pytest.fixture
def test_order(mocker):
    return mocker.Mock(currency="USD", incl_tax=D('100'))


@pytest.fixture
def test_address(mocker):
    return mocker.Mock(
        first_name="Bob", last_name="Buyer", line1='123 St', line3=None,
        line4='admin_area', postcode='33596', country=mocker.Mock(code='US'))
